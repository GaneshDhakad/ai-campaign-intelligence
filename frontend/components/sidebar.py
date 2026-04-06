"""
Sidebar Configuration Panel
"""
import streamlit as st


def render_sidebar():
    """Render the sidebar control panel."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.3rem;">🎯</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #e8e8f0;
                        background: linear-gradient(135deg, #818cf8, #c084fc);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Campaign IQ
            </div>
            <div style="font-size: 0.7rem; color: #5a5a7a; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.2rem;">
                Intelligence Engine v2.0
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # API Status
        st.markdown("##### ⚡ System Status")

        try:
            import httpx
            r = httpx.get("https://ai-campaign-intelligence.onrender.com/health", timeout=2)
            if r.status_code == 200:
                data = r.json()
                ml_icon = "🟢" if data.get('ml_model_loaded') else "🔴"
                nlp_icon = "🟢" if data.get('nlp_model_loaded') else "🔴"
                db_icon = "🟢" if data.get('database_connected') else "🔴"
                st.markdown(f"""
                {ml_icon} ML Engine  
                {nlp_icon} NLP Engine  
                {db_icon} Database
                """)
            else:
                st.warning("API degraded")
        except Exception:
            st.error("⚠️ Backend offline")
            st.caption("Start: `uvicorn backend.main:app`")

        st.markdown("---")

        st.markdown("""
        ##### 🔗 Navigation  
        Use the sidebar pages above ↑ to navigate.  

        **Pages:**  
        🏠 Dashboard • 🎯 Predict  
        📦 Batch • 💬 Sentiment  
        📊 Analytics • 🧪 Simulator  
        👥 Segments
        """)

        st.markdown("---")

        st.markdown("""
        <div style="text-align: center; padding: 0.5rem 0; color: #5a5a7a; font-size: 0.7rem;">
            Built with FastAPI + Streamlit<br/>
            XGBoost • VADER • SHAP
        </div>
        """, unsafe_allow_html=True)
