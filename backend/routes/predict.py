"""
Prediction Routes — /predict, /batch_predict
"""
import sys, os, io, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd

from backend.models.schemas import PredictRequest, PredictResponse, BatchPredictResponse
from backend.database.connection import store_prediction, store_batch_job

router = APIRouter(tags=["Prediction"])

# These will be set by main.py on startup
predictor = None
segmenter = None


@router.post("/predict", response_model=PredictResponse)
async def predict_customer(req: PredictRequest):
    """Predict single customer campaign response with SHAP explanation."""
    if predictor is None:
        raise HTTPException(503, "ML model not loaded")

    input_data = req.model_dump()
    result = predictor.predict(input_data)

    # SHAP values
    try:
        shap_data = predictor.get_shap_values(input_data)
        result['shap_values'] = shap_data['shap_values'] if shap_data else None
    except Exception:
        result['shap_values'] = None

    # Feature importance
    result['feature_importance'] = predictor.get_feature_importance()

    # Segment
    if segmenter:
        try:
            result['segment'] = segmenter.predict_single(input_data)
        except Exception:
            result['segment'] = None

    # Persist
    try:
        store_prediction(input_data, result,
                         segment_id=result.get('segment', {}).get('segment_id'))
    except Exception:
        pass

    return result


@router.post("/batch_predict", response_model=BatchPredictResponse)
async def batch_predict(file: UploadFile = File(...)):
    """Batch predict from CSV upload."""
    if predictor is None:
        raise HTTPException(503, "ML model not loaded")

    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only CSV files accepted")

    content = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(400, f"Failed to parse CSV: {e}")

    results_list = []
    for idx, row in df.iterrows():
        try:
            r = predictor.predict(row.to_dict())
            r['row_index'] = idx
            results_list.append(r)
        except Exception as e:
            results_list.append({'row_index': idx, 'error': str(e)})

    valid = [r for r in results_list if 'probability' in r]
    avg_prob = sum(r['probability'] for r in valid) / len(valid) if valid else 0
    respond = sum(1 for r in valid if r['prediction'] == 'Will Respond')

    # Persist batch job
    try:
        store_batch_job(file.filename, len(results_list), avg_prob, respond)
    except Exception:
        pass

    return BatchPredictResponse(
        total=len(results_list),
        avg_probability=round(avg_prob, 2),
        respond_count=respond,
        not_respond_count=len(valid) - respond,
        results=results_list
    )
