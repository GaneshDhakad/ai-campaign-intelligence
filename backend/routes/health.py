"""
Health Check Route — /health
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import APIRouter
from datetime import datetime
from backend.models.schemas import HealthResponse

router = APIRouter(tags=["System"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """System health check."""
    from backend.routes.predict import predictor
    from backend.routes.sentiment import sentiment_engine
    from backend.database.connection import get_connection

    db_ok = False
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
            db_ok = True
    except Exception:
        pass

    return HealthResponse(
        status="healthy" if all([predictor, sentiment_engine, db_ok]) else "degraded",
        ml_model_loaded=predictor is not None and predictor.model is not None,
        nlp_model_loaded=sentiment_engine is not None and sentiment_engine.is_trained,
        database_connected=db_ok,
        timestamp=datetime.now().isoformat()
    )
