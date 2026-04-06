"""
FastAPI Application — AI Campaign Intelligence Engine
======================================================
Main entry point for the backend API server.

Usage:
    uvicorn backend.main:app --reload --port 8000
"""
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.model_utils import CustomerResponsePredictor
from core.sentiment_engine import SentimentEngine
from core.segmentation import CustomerSegmenter

from backend.database.connection import init_db
from backend.routes import predict, sentiment, analytics, health

import pandas as pd


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load models and initialize database on startup."""
    print("\n🚀 Starting AI Campaign Intelligence Engine...")

    # Initialize database
    init_db()

    # Load ML model
    try:
        ml = CustomerResponsePredictor()
        ml.load('artifacts/model_artifacts.pkl')
        predict.predictor = ml
        print("  ✓ ML model loaded")
    except Exception as e:
        print(f"  ✗ ML model failed: {e}")

    # Load NLP engine
    try:
        nlp = SentimentEngine()
        nlp.load('artifacts/nlp_artifacts.pkl')
        sentiment.sentiment_engine = nlp
        print("  ✓ NLP engine loaded")
    except Exception as e:
        print(f"  ✗ NLP engine failed: {e}")

    # Initialize segmenter
    try:
        data_path = 'data/marketing_campaign.csv'
        if os.path.exists(data_path):
            df = pd.read_csv(data_path, sep='\t')
            from core.model_utils import preprocess_data, engineer_features
            df_clean, _ = preprocess_data(df)
            df_feat = engineer_features(df_clean)
            seg = CustomerSegmenter()
            seg.fit(df_feat)
            predict.segmenter = seg
            print("  ✓ Segmenter initialized")
    except Exception as e:
        print(f"  ✗ Segmenter failed: {e}")

    print("\n✅ Engine ready — http://localhost:8000/docs\n")

    yield  # App is running

    print("\n🛑 Shutting down...")


# ── FastAPI App ──────────────────────────────────

app = FastAPI(
    title="AI Campaign Intelligence Engine",
    description="Predict customer campaign response, analyze sentiment, and generate business recommendations.",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(predict.router)
app.include_router(sentiment.router)
app.include_router(analytics.router)
app.include_router(health.router)


@app.get("/")
async def root():
    return {
        "name": "AI Campaign Intelligence Engine",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }
