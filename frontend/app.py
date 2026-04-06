"""
AI Campaign Intelligence Engine — Main Dashboard
==================================================
Usage: streamlit run frontend/app.py (from project root)
"""
import sys, os

# Ensure project root and frontend dir are in path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import httpx
from datetime import datetime

st.set_page_config(
    page_title="Campaign IQ — AI Intelligence Engine",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

from components.theme import inject_theme
from components.kpi_cards import kpi_card, hero_banner
from components.sidebar import render_sidebar

inject_theme()
render_sidebar()

# ── Hero Banner ──
st.markdown(hero_banner(
    "🎯 Campaign Intelligence Engine",
    "AI-powered customer insights • Predictive analytics • Sentiment analysis"
), unsafe_allow_html=True)

# ── KPI Summary ──
try:
    r = httpx.get("http://localhost:8000/analytics/summary", timeout=3)
    if r.status_code == 200:
        data = r.json()
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown(kpi_card("Total Predictions", str(data.get('total_predictions', 0)),
                                 icon="📊", color="blue"), unsafe_allow_html=True)
        with c2:
            st.markdown(kpi_card("Avg Probability", f"{data.get('avg_probability', 0)}%",
                                 icon="🎯", color="purple"), unsafe_allow_html=True)
        with c3:
            st.markdown(kpi_card("Response Rate", f"{data.get('respond_rate', 0)}%",
                                 icon="✅", color="green"), unsafe_allow_html=True)
        with c4:
            st.markdown(kpi_card("Sentiments Analyzed", str(data.get('total_sentiments', 0)),
                                 icon="💬", color="cyan"), unsafe_allow_html=True)
        with c5:
            st.markdown(kpi_card("Avg Sentiment", f"{data.get('avg_sentiment', 0):+.2f}",
                                 icon="😊", color="amber"), unsafe_allow_html=True)
    else:
        st.info("📡 Connect to backend for live KPIs")
except Exception:
    st.info("📡 Start the backend server to see live dashboard data")
    st.code("uvicorn backend.main:app --reload --port 8000", language="bash")

st.markdown("---")

# ── Quick Actions ──
st.markdown("### ⚡ Quick Actions")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding: 2rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎯</div>
        <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">Predict Response</div>
        <div style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.3rem;">
            Single customer prediction with SHAP explainability
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding: 2rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💬</div>
        <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">Analyze Sentiment</div>
        <div style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.3rem;">
            VADER-powered sentiment with keyword extraction
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding: 2rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🧪</div>
        <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-primary);">Campaign Simulator</div>
        <div style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.3rem;">
            What-if analysis with ROI prediction engine
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Recent Activity ──
st.markdown("---")
st.markdown("### 📋 Recent Predictions")

try:
    r = httpx.get("http://localhost:8000/analytics/history?limit=5", timeout=3)
    if r.status_code == 200:
        history = r.json()
        if history:
            import pandas as pd
            df = pd.DataFrame(history)
            display_cols = ['timestamp', 'prediction', 'probability', 'risk_level']
            available = [c for c in display_cols if c in df.columns]
            st.dataframe(df[available], use_container_width=True, hide_index=True)
        else:
            st.caption("No predictions yet. Use the sidebar to navigate to the Predict page!")
except Exception:
    st.caption("📡 Backend offline — history unavailable")

# ── Footer ──
st.markdown(f"""
<div class="engine-footer">
    🎯 Campaign Intelligence Engine v2.0 • Built with XGBoost, VADER, SHAP, FastAPI & Streamlit
    <br/>© {datetime.now().year} AI Campaign IQ
</div>
""", unsafe_allow_html=True)
