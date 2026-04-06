"""
👥 Customer Segments — KMeans Cluster Visualization
"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Segments | Campaign IQ", page_icon="👥", layout="wide")
from components.theme import inject_theme
from components.kpi_cards import kpi_card
from components.charts import donut_chart
from components.sidebar import render_sidebar

inject_theme()
render_sidebar()

st.markdown("## 👥 Customer Segmentation")
st.caption("KMeans clustering analysis — understand your customer base")

try:
    from core.model_utils import preprocess_data, engineer_features
    from core.segmentation import CustomerSegmenter, SEGMENT_PROFILES

    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'marketing_campaign.csv')

    if os.path.exists(data_path):
        df = pd.read_csv(data_path, sep='\t')
        df_clean, y = preprocess_data(df)
        df_feat = engineer_features(df_clean)

        seg = CustomerSegmenter()
        seg.fit(df_feat)
        summaries = seg.get_segment_summary(df_feat)

        # Segment KPI cards
        cols = st.columns(4)
        for i, s in enumerate(summaries):
            with cols[i]:
                colors = ["purple", "green", "blue", "red"]
                st.markdown(kpi_card(
                    f"{s['icon']} {s['name']}",
                    f"{s['count']} ({s['pct']}%)",
                    color=colors[i],
                    icon=s['icon']
                ), unsafe_allow_html=True)

        st.markdown("---")

        # Distribution donut
        col1, col2 = st.columns(2)
        with col1:
            labels = [s['name'] for s in summaries]
            values = [s['count'] for s in summaries]
            colors_list = [s['color'] for s in summaries]
            fig = donut_chart(labels, values, "Segment Distribution", colors_list)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Segment details
            for s in summaries:
                with st.expander(f"{s['icon']} {s['name']} — {s['count']} customers"):
                    st.write(f"**Strategy:** {s['strategy']}")
                    if s.get('metrics'):
                        for feat, vals in s['metrics'].items():
                            st.write(f"  • {feat}: mean={vals['mean']:,.0f}, median={vals['median']:,.0f}")

        # Scatter plot
        st.markdown("---")
        st.markdown("### 🔍 Segment Scatter Analysis")
        df_feat['Segment'] = seg.predict(df_feat)
        seg_names = {i: SEGMENT_PROFILES[i]['name'] for i in range(4)}
        df_feat['Segment_Name'] = df_feat['Segment'].map(seg_names)

        import plotly.express as px
        c1, c2 = st.columns(2)
        x_axis = c1.selectbox("X-Axis", ['CLV', 'Income', 'Purchase_Frequency', 'Engagement_Score'], index=0)
        y_axis = c2.selectbox("Y-Axis", ['Engagement_Score', 'CLV', 'Income', 'Recency'], index=0)

        fig = px.scatter(df_feat, x=x_axis, y=y_axis, color='Segment_Name',
                         color_discrete_sequence=['#FFD700', '#4CAF50', '#2196F3', '#F44336'],
                         opacity=0.6, hover_data=['Income', 'CLV'])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e8e8f0'), height=500,
            xaxis=dict(gridcolor='rgba(255,255,255,0.06)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.06)')
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"Dataset not found at: {data_path}")

except Exception as e:
    st.error(f"Error loading segmentation: {e}")
    import traceback
    st.code(traceback.format_exc())
