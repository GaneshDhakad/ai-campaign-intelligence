"""
Pydantic Schemas — Request/Response Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ── Prediction ────────────────────────────────────

class PredictRequest(BaseModel):
    Income: float = Field(60000, description="Annual income ($)")
    Age: int = Field(45, description="Customer age")
    Education: int = Field(3, description="1=Basic, 2=2nCycle, 3=Grad, 4=Master, 5=PhD")
    Is_Partnered: int = Field(1, description="1=Yes, 0=No")
    CLV: float = Field(800, description="Customer Lifetime Value ($)")
    Purchase_Frequency: int = Field(10, description="Total purchases")
    Recency: int = Field(30, description="Days since last purchase")
    Engagement_Score: float = Field(60, description="0-100 engagement score")
    Campaign_Acceptance_Rate: float = Field(0.2, description="0.0-1.0")
    Customer_Days: int = Field(500, description="Tenure in days")


class PredictResponse(BaseModel):
    prediction: str
    probability: float
    probability_raw: float
    risk_level: str
    recommendation: str
    action: str
    color: str
    shap_values: Optional[Dict[str, float]] = None
    feature_importance: Optional[Dict[str, float]] = None
    segment: Optional[Dict[str, Any]] = None


# ── Batch Prediction ─────────────────────────────

class BatchPredictResponse(BaseModel):
    total: int
    avg_probability: float
    respond_count: int
    not_respond_count: int
    results: List[Dict[str, Any]]


# ── Sentiment ────────────────────────────────────

class SentimentRequest(BaseModel):
    text: str = Field(..., description="Customer feedback text")


class SentimentResponse(BaseModel):
    label: int
    label_text: str
    compound: float
    confidence: float
    pos: float
    neg: float
    neu: float
    intensity: str
    keywords: Dict[str, List[str]]


# ── Analytics ────────────────────────────────────

class SimulationRequest(BaseModel):
    target_segments: List[int] = Field([0, 1], description="Segment IDs to target")
    budget: float = Field(10000, description="Campaign budget ($)")
    channel: str = Field("email", description="Campaign channel")


class SimulationResponse(BaseModel):
    estimated_reach: int
    estimated_responders: int
    estimated_response_rate: float
    estimated_roi: float
    cost_per_acquisition: float
    recommendation: str


# ── Health ───────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    ml_model_loaded: bool
    nlp_model_loaded: bool
    database_connected: bool
    timestamp: str
