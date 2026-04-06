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

# ✅ LIVE BACKEND URL (UPDATED)
API_URL = "https://ai-campaign-intelligence.onrender.com"

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
    r = httpx.get(f"{API_URL}/analytics/summary", timeout=10)
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
        st.warning("⚠️ Backend connected but returned an error")
except Exception:
    st.error("🚫 Cannot connect to backend (Render may be sleeping)")

st.markdown("---")

# ── Quick Actions ──
st.markdown("### ⚡ Quick Actions")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding: 2rem;">
        <div style="font-size: 2.5rem;">🎯</div>
        <div style="font-weight: 600;">Predict Response</div>
        <div style="font-size: 0.85rem;">Single customer prediction</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding: 2rem;">
        <div style="font-size: 2.5rem;">💬</div>
        <div style="font-weight: 600;">Analyze Sentiment</div>
        <div style="font-size: 0.85rem;">VADER sentiment engine</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding: 2rem;">
        <div style="font-size: 2.5rem;">🧪</div>
        <div style="font-weight: 600;">Campaign Simulator</div>
        <div style="font-size: 0.85rem;">ROI what-if analysis</div>
    </div>
    """, unsafe_allow_html=True)

# ── Recent Activity ──
st.markdown("---")
st.markdown("### 📋 Recent Predictions")

try:
    r = httpx.get(f"{API_URL}/analytics/history?limit=5", timeout=10)
    if r.status_code == 200:
        history = r.json()
        if history:
            import pandas as pd
            df = pd.DataFrame(history)
            display_cols = ['timestamp', 'prediction', 'probability', 'risk_level']
            available = [c for c in display_cols if c in df.columns]
            st.dataframe(df[available], use_container_width=True, hide_index=True)
        else:
            st.caption("No predictions yet.")
except Exception:
    st.caption("Backend sleeping or unreachable")

# ── Footer ──
st.markdown(f"""
<div class="engine-footer">
    🎯 Campaign Intelligence Engine v2.0 • FastAPI + Streamlit
    <br/>© {datetime.now().year}
</div>
""", unsafe_allow_html=True)
