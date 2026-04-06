"""
💬 Sentiment Analysis — VADER-powered with keyword highlighting
"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import httpx

st.set_page_config(page_title="Sentiment | Campaign IQ", page_icon="💬", layout="wide")
from components.theme import inject_theme
from components.kpi_cards import kpi_card, sentiment_badge
from components.charts import sentiment_gauge, sentiment_breakdown_bars
from components.sidebar import render_sidebar

inject_theme()
render_sidebar()

API = "http://localhost:8000"

st.markdown("## 💬 Sentiment Analysis Engine")
st.caption("VADER + TF-IDF hybrid analysis with intensity scoring and keyword extraction")

col_in, col_out = st.columns([1, 1.3])

with col_in:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    text = st.text_area("Enter customer feedback, review, or social media post",
                        "The product quality is excellent and I love the fast shipping, "
                        "but the customer support was disappointing and unhelpful.",
                        height=150)

    # Quick templates
    with st.expander("📝 Quick Templates"):
        templates = {
            "Highly Positive": "Absolutely amazing product! Best purchase I've ever made. The quality is outstanding and delivery was super fast!",
            "Mixed / Neutral": "The product is okay. Some features are nice but others need improvement. Decent value for money.",
            "Very Negative": "Terrible experience. Product broke after 2 days. Customer support is useless and refused to help. Complete waste of money.",
            "Complex Feedback": "I appreciate the innovative design and the team's effort, but the pricing is too high compared to competitors. Not interested in renewing."
        }
        for name, val in templates.items():
            if st.button(name, use_container_width=True):
                text = val

    analyze_btn = st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_out:
    if analyze_btn and text.strip():
        with st.spinner("Analyzing sentiment..."):
            try:
                r = httpx.post(f"{API}/sentiment", json={"text": text}, timeout=10)
                s = r.json()

                # Sentiment gauge
                st.plotly_chart(sentiment_gauge(s['compound'], s['pos'], s['neg'], s['neu']),
                                use_container_width=True)

                # Badge + intensity
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(sentiment_badge(s['label_text'], s['compound']), unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**Intensity:** {s['intensity']} | **Confidence:** {s['confidence']:.0%}")

                # KPI row
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(kpi_card("Positive", f"{s['pos']:.0%}", color="green", icon="😊"),
                                unsafe_allow_html=True)
                with c2:
                    st.markdown(kpi_card("Neutral", f"{s['neu']:.0%}", color="blue", icon="😐"),
                                unsafe_allow_html=True)
                with c3:
                    st.markdown(kpi_card("Negative", f"{s['neg']:.0%}", color="red", icon="😟"),
                                unsafe_allow_html=True)
                with c4:
                    st.markdown(kpi_card("Compound", f"{s['compound']:+.3f}", color="purple", icon="📊"),
                                unsafe_allow_html=True)

                # Breakdown bars
                st.plotly_chart(sentiment_breakdown_bars(s['pos'], s['neg'], s['neu']),
                                use_container_width=True)

                # Keywords
                st.markdown("---")
                st.markdown("##### 🔑 Key Sentiment Drivers")
                kw = s.get('keywords', {})
                c1, c2 = st.columns(2)
                with c1:
                    pos_words = kw.get('positive', [])
                    if pos_words:
                        for w in pos_words:
                            st.markdown(f'<span class="sentiment-badge sentiment-positive">{w}</span> ',
                                        unsafe_allow_html=True)
                    else:
                        st.caption("No strong positive keywords detected")
                with c2:
                    neg_words = kw.get('negative', [])
                    if neg_words:
                        for w in neg_words:
                            st.markdown(f'<span class="sentiment-badge sentiment-negative">{w}</span> ',
                                        unsafe_allow_html=True)
                    else:
                        st.caption("No strong negative keywords detected")

                # Engine details
                with st.expander("⚙️ Engine Details"):
                    st.json(s)

            except httpx.ConnectError:
                st.error("⚠️ Backend offline.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem;">💬</div>
            <h3>Enter Text to Analyze</h3>
            <p style="color: var(--text-secondary);">Paste customer feedback, reviews, or social media posts</p>
        </div>
        """, unsafe_allow_html=True)
