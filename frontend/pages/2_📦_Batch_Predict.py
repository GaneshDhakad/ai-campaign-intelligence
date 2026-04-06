"""
📦 Batch Predict — CSV Upload for Bulk Predictions
"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import httpx
import pandas as pd
import io

st.set_page_config(page_title="Batch Predict | Campaign IQ", page_icon="📦", layout="wide")
from components.theme import inject_theme
from components.kpi_cards import kpi_card, hero_banner
from components.sidebar import render_sidebar

inject_theme()
render_sidebar()

API = "http://localhost:8000"

st.markdown("## 📦 Batch Prediction")
st.caption("Upload a CSV file to score multiple customers at once")

# Upload section
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

uploaded = st.file_uploader("Upload Customer CSV", type=['csv'], help="CSV with customer feature columns")

if uploaded:
    df_preview = pd.read_csv(uploaded)
    st.markdown(f"**Preview** — {len(df_preview)} rows, {len(df_preview.columns)} columns")
    st.dataframe(df_preview.head(10), use_container_width=True, hide_index=True)

    if st.button("🚀 Run Batch Prediction", type="primary", use_container_width=True):
        uploaded.seek(0)
        with st.spinner(f"Scoring {len(df_preview)} customers..."):
            try:
                files = {"file": (uploaded.name, uploaded.getvalue(), "text/csv")}
                r = httpx.post(f"{API}/batch_predict", files=files, timeout=120)
                result = r.json()

                st.success(f"✅ Batch complete — {result['total']} customers scored")

                # KPIs
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(kpi_card("Total", str(result['total']), icon="📋", color="blue"),
                                unsafe_allow_html=True)
                with c2:
                    st.markdown(kpi_card("Avg Probability", f"{result['avg_probability']}%", icon="📊", color="purple"),
                                unsafe_allow_html=True)
                with c3:
                    st.markdown(kpi_card("Will Respond", str(result['respond_count']), icon="✅", color="green"),
                                unsafe_allow_html=True)
                with c4:
                    st.markdown(kpi_card("Won't Respond", str(result['not_respond_count']), icon="❌", color="red"),
                                unsafe_allow_html=True)

                # Results table
                st.markdown("---")
                results_df = pd.DataFrame(result['results'])
                st.dataframe(results_df, use_container_width=True, hide_index=True)

                # Download
                csv_bytes = results_df.to_csv(index=False).encode()
                st.download_button("📥 Download Results CSV", csv_bytes,
                                   "batch_predictions.csv", "text/csv",
                                   use_container_width=True)

            except httpx.ConnectError:
                st.error("⚠️ Backend offline.")
            except Exception as e:
                st.error(f"Error: {e}")

else:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📁</div>
        <p>Drag & drop a CSV file or click Browse</p>
        <p style="font-size: 0.8rem; color: var(--text-muted);">
            Required columns: Income, Age, Education, CLV, Purchase_Frequency, Recency, etc.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
