"""
📊 Analytics — Historical prediction analytics dashboard
"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import httpx
import pandas as pd

st.set_page_config(page_title="Analytics | Campaign IQ", page_icon="📊", layout="wide")
from components.theme import inject_theme
from components.kpi_cards import kpi_card
from components.charts import donut_chart, line_chart
from components.sidebar import render_sidebar

inject_theme()
render_sidebar()

API = "http://localhost:8000"

st.markdown("## 📊 Analytics Dashboard")
st.caption("Historical prediction data and performance trends")

try:
    # Summary KPIs
    r = httpx.get(f"{API}/analytics/summary", timeout=3)
    if r.status_code == 200:
        data = r.json()

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(kpi_card("Total Predictions", str(data['total_predictions']), icon="📋", color="blue"),
                        unsafe_allow_html=True)
        with c2:
            st.markdown(kpi_card("Avg Probability", f"{data['avg_probability']}%", icon="📊", color="purple"),
                        unsafe_allow_html=True)
        with c3:
            st.markdown(kpi_card("Response Rate", f"{data['respond_rate']}%", icon="✅", color="green"),
                        unsafe_allow_html=True)
        with c4:
            st.markdown(kpi_card("Sentiments", str(data['total_sentiments']), icon="💬", color="cyan"),
                        unsafe_allow_html=True)

    st.markdown("---")

    # Prediction History
    r2 = httpx.get(f"{API}/analytics/history?limit=100", timeout=3)
    if r2.status_code == 200:
        history = r2.json()
        if history:
            df = pd.DataFrame(history)

            col1, col2 = st.columns(2)

            with col1:
                # Response distribution
                respond = sum(1 for h in history if h.get('prediction') == 'Will Respond')
                not_respond = len(history) - respond
                fig = donut_chart(
                    ['Will Respond', 'Will Not Respond'],
                    [respond, not_respond],
                    title="Response Distribution",
                    colors=['#10b981', '#ef4444']
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Probability trend
                if 'probability' in df.columns and len(df) > 1:
                    fig = line_chart(
                        list(range(len(df))), df['probability'].tolist(),
                        title="Probability Trend", xlabel="Prediction #", ylabel="Probability %"
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # Full table
            st.markdown("### 📋 Prediction Log")
            display_cols = ['timestamp', 'prediction', 'probability', 'risk_level', 'recommendation']
            available = [c for c in display_cols if c in df.columns]
            st.dataframe(df[available], use_container_width=True, hide_index=True)
        else:
            st.info("No data yet. Make some predictions first!")

except httpx.ConnectError:
    st.error("⚠️ Backend offline. Start with: `uvicorn backend.main:app --reload --port 8000`")
except Exception as e:
    st.error(f"Error: {e}")
