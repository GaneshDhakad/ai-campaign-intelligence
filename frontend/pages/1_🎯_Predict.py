"""
🎯 Predict — Single Customer Prediction with SHAP
"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import httpx

st.set_page_config(page_title="Predict | Campaign IQ", page_icon="🎯", layout="wide")
from components.theme import inject_theme
from components.kpi_cards import kpi_card, recommendation_box, sentiment_badge
from components.charts import gauge_chart, shap_waterfall, feature_importance_bar
from components.sidebar import render_sidebar

inject_theme()
render_sidebar()

API = "http://localhost:8000"

st.markdown("## 🎯 Customer Response Prediction")
st.caption("Enter customer details to predict campaign response with AI explainability")

col_input, col_output = st.columns([1, 1.2])

with col_input:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 Manual Entry", "👤 Quick Profiles"])

    with tab1:
        st.markdown("##### Demographics")
        c1, c2 = st.columns(2)
        with c1:
            income = st.number_input("Annual Income ($)", 0, 200000, 60000, 5000)
            age = st.slider("Age", 18, 100, 45)
            education = st.selectbox("Education", [1,2,3,4,5], index=2,
                                     format_func=lambda x: {1:'Basic',2:'2n Cycle',3:'Grad',4:'Master',5:'PhD'}[x])
        with c2:
            is_partnered = st.checkbox("Has Partner", True)
            recency = st.slider("Recency (days)", 0, 100, 30)
            tenure = st.number_input("Tenure (days)", 0, 3000, 500)

        st.markdown("##### Purchase Behavior")
        c1, c2 = st.columns(2)
        with c1:
            clv = st.number_input("Lifetime Value ($)", 0, 10000, 800, 100)
            purchase_freq = st.number_input("Purchase Frequency", 0, 50, 10)
        with c2:
            engagement = st.slider("Engagement Score", 0, 100, 60)
            camp_acc = st.slider("Campaign Acceptance", 0.0, 1.0, 0.2, 0.05)

    with tab2:
        profile = st.radio("Select Profile", ["High-Value Champion", "Engaged Buyer", "Potential Star", "At-Risk"])
        profiles = {
            "High-Value Champion": dict(Income=90000, Age=42, Education=4, Is_Partnered=1, CLV=2500, Purchase_Frequency=25, Recency=10, Engagement_Score=85, Campaign_Acceptance_Rate=0.6, Customer_Days=1200),
            "Engaged Buyer": dict(Income=65000, Age=38, Education=3, Is_Partnered=1, CLV=1200, Purchase_Frequency=15, Recency=20, Engagement_Score=70, Campaign_Acceptance_Rate=0.4, Customer_Days=800),
            "Potential Star": dict(Income=85000, Age=35, Education=4, Is_Partnered=0, CLV=400, Purchase_Frequency=5, Recency=45, Engagement_Score=45, Campaign_Acceptance_Rate=0.1, Customer_Days=200),
            "At-Risk": dict(Income=40000, Age=52, Education=2, Is_Partnered=1, CLV=150, Purchase_Frequency=2, Recency=85, Engagement_Score=20, Campaign_Acceptance_Rate=0.0, Customer_Days=300),
        }
        if profile:
            p = profiles[profile]
            income, age, education, is_partnered = p['Income'], p['Age'], p['Education'], p['Is_Partnered']
            clv, purchase_freq, recency = p['CLV'], p['Purchase_Frequency'], p['Recency']
            engagement, camp_acc, tenure = p['Engagement_Score'], p['Campaign_Acceptance_Rate'], p['Customer_Days']

    st.markdown("---")

    # Sentiment input
    st.markdown("##### 💬 Customer Feedback")
    feedback = st.text_area("Enter customer feedback text", "I love the quality but the pricing is a bit high for my budget.",
                            height=80)

    predict_btn = st.button("🎯 Analyze & Predict", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col_output:
    if predict_btn:
        payload = {
            "Income": income, "Age": age, "Education": education,
            "Is_Partnered": int(is_partnered), "CLV": clv,
            "Purchase_Frequency": purchase_freq, "Recency": recency,
            "Engagement_Score": engagement,
            "Campaign_Acceptance_Rate": camp_acc, "Customer_Days": tenure
        }

        with st.spinner("🔮 Running AI analysis..."):
            try:
                # Prediction
                r = httpx.post(f"{API}/predict", json=payload, timeout=15)
                result = r.json()

                # Sentiment
                sr = httpx.post(f"{API}/sentiment", json={"text": feedback}, timeout=5)
                sent = sr.json()

                # ── Gauge ──
                st.plotly_chart(gauge_chart(result['probability']), use_container_width=True)

                # ── KPI Row ──
                c1, c2, c3 = st.columns(3)
                with c1:
                    color = "green" if result['probability'] >= 50 else "red"
                    st.markdown(kpi_card("Prediction", result['prediction'], color=color, icon="🎯"),
                                unsafe_allow_html=True)
                with c2:
                    st.markdown(kpi_card("Probability", f"{result['probability']}%", color="purple", icon="📊"),
                                unsafe_allow_html=True)
                with c3:
                    st.markdown(kpi_card("Action", result['action'], color="amber", icon="⚡"),
                                unsafe_allow_html=True)

                # ── Sentiment ──
                st.markdown("---")
                st.markdown(sentiment_badge(sent['label_text'], sent['compound']), unsafe_allow_html=True)

                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    st.metric("Positive", f"{sent['pos']:.0%}")
                with sc2:
                    st.metric("Neutral", f"{sent['neu']:.0%}")
                with sc3:
                    st.metric("Negative", f"{sent['neg']:.0%}")

                if sent.get('keywords'):
                    kw = sent['keywords']
                    if kw.get('positive'):
                        st.success(f"✅ Positive: {', '.join(kw['positive'])}")
                    if kw.get('negative'):
                        st.error(f"⚠️ Negative: {', '.join(kw['negative'])}")

                # ── Recommendation ──
                rec_text = result['recommendation']
                if sent['label'] == -1:
                    rec_text = "⚠️ Negative sentiment detected — " + rec_text
                level = "high" if result['probability'] >= 75 else "medium" if result['probability'] >= 50 else "low"
                st.markdown(recommendation_box(rec_text, level), unsafe_allow_html=True)

                # ── SHAP ──
                if result.get('shap_values'):
                    with st.expander("🔍 SHAP Explainability — Why this prediction?"):
                        sv = result['shap_values']
                        fig = shap_waterfall(list(sv.keys()), list(sv.values()), 0)
                        st.plotly_chart(fig, use_container_width=True)

                # ── Feature Importance ──
                if result.get('feature_importance'):
                    with st.expander("📊 Feature Importance — What matters most?"):
                        fig = feature_importance_bar(result['feature_importance'])
                        st.plotly_chart(fig, use_container_width=True)

                # ── Segment ──
                if result.get('segment'):
                    seg = result['segment']
                    st.markdown(f"""
                    <div class="glass-card" style="margin-top: 1rem;">
                        <span style="font-size: 1.5rem;">{seg.get('icon','📊')}</span>
                        <strong>{seg.get('name','Unknown')}</strong>
                        <br/><span style="color: var(--text-secondary); font-size: 0.85rem;">{seg.get('strategy','')}</span>
                    </div>
                    """, unsafe_allow_html=True)

            except httpx.ConnectError:
                st.error("⚠️ Backend offline. Start with: `uvicorn backend.main:app --reload --port 8000`")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="color: var(--text-primary);">Ready to Predict</h3>
            <p style="color: var(--text-secondary);">
                Enter customer details on the left and click <strong>Analyze & Predict</strong>
                to see AI-powered insights with SHAP explainability.
            </p>
        </div>
        """, unsafe_allow_html=True)
