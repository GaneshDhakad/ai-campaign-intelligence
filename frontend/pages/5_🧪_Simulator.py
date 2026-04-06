"""
🧪 Campaign Simulator — What-if ROI Analysis
"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import httpx

st.set_page_config(page_title="Simulator | Campaign IQ", page_icon="🧪", layout="wide")
from components.theme import inject_theme
from components.kpi_cards import kpi_card, recommendation_box
from components.sidebar import render_sidebar

inject_theme()
render_sidebar()

API = "http://localhost:8000"

st.markdown("## 🧪 Campaign Simulator")
st.caption("What-if analysis with ROI prediction — test targeting strategies before launch")

col_config, col_result = st.columns([1, 1.2])

with col_config:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown("##### Target Segments")
    seg_options = {
        0: "👑 Premium Champions (65% response)",
        1: "🛒 Engaged Buyers (45% response)",
        2: "⭐ Potential Stars (25% response)",
        3: "⚠️ At-Risk Customers (10% response)"
    }
    selected = []
    for seg_id, label in seg_options.items():
        if st.checkbox(label, value=seg_id <= 1):
            selected.append(seg_id)

    st.markdown("---")
    st.markdown("##### Campaign Configuration")
    budget = st.slider("💰 Budget ($)", 1000, 100000, 15000, 1000)
    channel = st.selectbox("📡 Channel", ["email", "sms", "direct_mail"],
                           format_func=lambda x: {"email": "📧 Email ($2.5/contact)",
                                                  "sms": "📱 SMS ($8/contact)",
                                                  "direct_mail": "📬 Direct Mail ($15/contact)"}[x])

    simulate_btn = st.button("🚀 Simulate Campaign", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_result:
    if simulate_btn and selected:
        with st.spinner("Running simulation..."):
            try:
                r = httpx.post(f"{API}/analytics/simulate", json={
                    "target_segments": selected,
                    "budget": budget,
                    "channel": channel
                }, timeout=10)
                sim = r.json()

                # KPIs
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(kpi_card("Est. Reach", f"{sim['estimated_reach']:,}", icon="👥", color="blue"),
                                unsafe_allow_html=True)
                with c2:
                    st.markdown(kpi_card("Est. Responders", f"{sim['estimated_responders']:,}", icon="✅", color="green"),
                                unsafe_allow_html=True)
                with c3:
                    roi_color = "green" if sim['estimated_roi'] > 0 else "red"
                    st.markdown(kpi_card("Est. ROI", f"{sim['estimated_roi']}%", icon="📈", color=roi_color),
                                unsafe_allow_html=True)

                st.markdown("---")

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(kpi_card("Response Rate", f"{sim['estimated_response_rate']}%", icon="🎯", color="purple"),
                                unsafe_allow_html=True)
                with c2:
                    st.markdown(kpi_card("Cost/Acquisition", f"${sim['cost_per_acquisition']}", icon="💵", color="amber"),
                                unsafe_allow_html=True)

                # Recommendation
                level = "high" if sim['estimated_roi'] > 100 else "medium" if sim['estimated_roi'] > 0 else "low"
                st.markdown(recommendation_box(sim['recommendation'], level), unsafe_allow_html=True)

                # Budget breakdown
                with st.expander("💰 Budget Breakdown"):
                    cost_per = {"email": 2.5, "sms": 8.0, "direct_mail": 15.0}[channel]
                    st.write(f"**Channel:** {channel.replace('_',' ').title()}")
                    st.write(f"**Cost per Contact:** ${cost_per}")
                    st.write(f"**Total Budget:** ${budget:,}")
                    st.write(f"**Max Contacts:** {int(budget / cost_per):,}")
                    st.write(f"**Revenue per Response:** ~$85")

            except httpx.ConnectError:
                st.error("⚠️ Backend offline.")
            except Exception as e:
                st.error(f"Error: {e}")
    elif simulate_btn:
        st.warning("Select at least one segment to target")
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem;">🧪</div>
            <h3>Campaign Simulation Lab</h3>
            <p style="color: var(--text-secondary);">Configure segments, budget, and channel to simulate campaign ROI</p>
        </div>
        """, unsafe_allow_html=True)
