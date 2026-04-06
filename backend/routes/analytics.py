"""
Analytics Routes — /analytics/summary, /analytics/history, /analytics/simulate
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import APIRouter, HTTPException
from backend.models.schemas import SimulationRequest, SimulationResponse
from backend.database.connection import get_analytics_summary, get_prediction_history

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
async def analytics_summary():
    """Get aggregate analytics summary."""
    try:
        return get_analytics_summary()
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/history")
async def prediction_history(limit: int = 50):
    """Get recent prediction history."""
    try:
        return get_prediction_history(limit)
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/simulate", response_model=SimulationResponse)
async def campaign_simulation(req: SimulationRequest):
    """What-if campaign simulation."""
    # Segment average response rates (from training data analysis)
    segment_rates = {0: 0.65, 1: 0.45, 2: 0.25, 3: 0.10}
    segment_sizes = {0: 180, 1: 450, 2: 600, 3: 970}  # approximate from dataset

    total_reach = sum(segment_sizes.get(s, 0) for s in req.target_segments)
    avg_rate = sum(segment_rates.get(s, 0.1) for s in req.target_segments) / max(len(req.target_segments), 1)
    estimated_responders = int(total_reach * avg_rate)

    cost_per_contact = 2.5 if req.channel == "email" else 8.0 if req.channel == "sms" else 15.0
    total_cost = min(total_reach * cost_per_contact, req.budget)
    actual_reach = int(total_cost / cost_per_contact)
    actual_responders = int(actual_reach * avg_rate)

    avg_revenue_per_response = 85.0
    revenue = actual_responders * avg_revenue_per_response
    roi = ((revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0
    cpa = total_cost / actual_responders if actual_responders > 0 else 0

    if roi > 200:
        rec = "🚀 Excellent ROI — Execute immediately with full budget"
    elif roi > 100:
        rec = "✅ Strong ROI — Recommended for execution"
    elif roi > 0:
        rec = "⚠️ Moderate ROI — Consider optimizing targeting"
    else:
        rec = "❌ Negative ROI — Reassess segment selection or channel"

    return SimulationResponse(
        estimated_reach=actual_reach,
        estimated_responders=actual_responders,
        estimated_response_rate=round(avg_rate * 100, 1),
        estimated_roi=round(roi, 1),
        cost_per_acquisition=round(cpa, 2),
        recommendation=rec
    )
