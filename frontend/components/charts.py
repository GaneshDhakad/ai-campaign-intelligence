"""
Plotly Chart Builders — Dark-themed interactive charts
"""
import plotly.graph_objects as go
import plotly.express as px
from frontend.components.theme import PLOTLY_DARK_TEMPLATE


def _apply_dark(fig, height=350):
    """Apply dark theme to any Plotly figure."""
    fig.update_layout(
        **PLOTLY_DARK_TEMPLATE['layout'],
        height=height,
        showlegend=True,
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8b8ba7'))
    )
    return fig


def gauge_chart(value: float, title: str = "Response Probability", height=300):
    """Premium gauge chart for probability."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': '%', 'font': {'size': 48, 'color': '#e8e8f0', 'family': 'Inter'}},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 14, 'color': '#8b8ba7'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#5a5a7a', 'tickwidth': 1},
            'bar': {'color': '#6366f1', 'thickness': 0.8},
            'bgcolor': 'rgba(255,255,255,0.03)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 25], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [25, 50], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [50, 75], 'color': 'rgba(99, 102, 241, 0.15)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ],
            'threshold': {
                'line': {'color': '#ef4444', 'width': 3},
                'thickness': 0.8,
                'value': 50
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        margin=dict(l=30, r=30, t=40, b=10)
    )
    return fig


def shap_waterfall(feature_names: list, shap_values: list, base_value: float, height=400):
    """SHAP waterfall chart for feature contributions."""
    sorted_pairs = sorted(zip(feature_names, shap_values), key=lambda x: abs(x[1]))
    names = [p[0] for p in sorted_pairs]
    values = [p[1] for p in sorted_pairs]
    colors = ['#10b981' if v > 0 else '#ef4444' for v in values]

    fig = go.Figure(go.Bar(
        x=values, y=names, orientation='h',
        marker_color=colors,
        text=[f'{v:+.3f}' for v in values],
        textposition='outside',
        textfont=dict(color='#e8e8f0', size=11)
    ))
    fig.update_layout(
        title=dict(text='Feature Impact (SHAP)', font=dict(size=14, color='#8b8ba7')),
        xaxis_title='SHAP Value',
    )
    return _apply_dark(fig, height)


def feature_importance_bar(importance_dict: dict, height=350):
    """Horizontal bar chart for feature importance."""
    sorted_items = sorted(importance_dict.items(), key=lambda x: x[1])
    names = [i[0] for i in sorted_items]
    values = [i[1] for i in sorted_items]

    fig = go.Figure(go.Bar(
        x=values, y=names, orientation='h',
        marker=dict(
            color=values,
            colorscale=[[0, '#6366f1'], [0.5, '#8b5cf6'], [1, '#c084fc']],
        ),
        text=[f'{v:.3f}' for v in values],
        textposition='outside',
        textfont=dict(color='#e8e8f0', size=11)
    ))
    fig.update_layout(
        title=dict(text='Feature Importance', font=dict(size=14, color='#8b8ba7')),
        xaxis_title='Importance Score',
    )
    return _apply_dark(fig, height)


def sentiment_gauge(compound: float, pos: float, neg: float, neu: float, height=250):
    """Compound sentiment score gauge."""
    color = '#10b981' if compound > 0.05 else '#ef4444' if compound < -0.05 else '#8b8ba7'
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=compound,
        number={'font': {'size': 40, 'color': color}},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': 'Sentiment Score', 'font': {'size': 13, 'color': '#8b8ba7'}},
        gauge={
            'axis': {'range': [-1, 1], 'tickcolor': '#5a5a7a'},
            'bar': {'color': color, 'thickness': 0.7},
            'bgcolor': 'rgba(255,255,255,0.03)',
            'borderwidth': 0,
            'steps': [
                {'range': [-1, -0.05], 'color': 'rgba(239, 68, 68, 0.12)'},
                {'range': [-0.05, 0.05], 'color': 'rgba(139, 139, 167, 0.08)'},
                {'range': [0.05, 1], 'color': 'rgba(16, 185, 129, 0.12)'}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      height=height, margin=dict(l=20, r=20, t=40, b=10))
    return fig


def sentiment_breakdown_bars(pos: float, neg: float, neu: float, height=200):
    """Stacked sentiment intensity bars."""
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Positive', x=[pos], y=['Breakdown'], orientation='h',
                         marker_color='#10b981', text=f'{pos:.0%}', textposition='inside'))
    fig.add_trace(go.Bar(name='Neutral', x=[neu], y=['Breakdown'], orientation='h',
                         marker_color='#5a5a7a', text=f'{neu:.0%}', textposition='inside'))
    fig.add_trace(go.Bar(name='Negative', x=[neg], y=['Breakdown'], orientation='h',
                         marker_color='#ef4444', text=f'{neg:.0%}', textposition='inside'))
    fig.update_layout(barmode='stack', showlegend=True)
    return _apply_dark(fig, height)


def donut_chart(labels: list, values: list, title: str = "", colors: list = None, height=350):
    """Donut chart for segment distribution."""
    if colors is None:
        colors = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#8b5cf6']
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.6,
        marker=dict(colors=colors[:len(labels)]),
        textinfo='label+percent',
        textfont=dict(color='#e8e8f0', size=12)
    ))
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=14, color='#8b8ba7')))
    return _apply_dark(fig, height)


def line_chart(x, y, title="", xlabel="", ylabel="", height=350):
    """Gradient line chart."""
    fig = go.Figure(go.Scatter(
        x=x, y=y, mode='lines+markers',
        line=dict(color='#6366f1', width=3),
        marker=dict(size=6, color='#818cf8'),
        fill='tozeroy',
        fillcolor='rgba(99, 102, 241, 0.1)'
    ))
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=14, color='#8b8ba7')))
    fig.update_layout(xaxis_title=xlabel, yaxis_title=ylabel)
    return _apply_dark(fig, height)
