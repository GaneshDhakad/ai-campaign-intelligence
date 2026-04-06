"""
Sentiment Routes — /sentiment
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import APIRouter, HTTPException
from backend.models.schemas import SentimentRequest, SentimentResponse
from backend.database.connection import store_sentiment

router = APIRouter(tags=["Sentiment"])

# Set by main.py on startup
sentiment_engine = None


@router.post("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(req: SentimentRequest):
    """Analyze sentiment of customer feedback text."""
    if sentiment_engine is None:
        raise HTTPException(503, "NLP model not loaded")

    result = sentiment_engine.analyze(req.text)

    # Persist
    try:
        store_sentiment(req.text, result)
    except Exception:
        pass

    return result
