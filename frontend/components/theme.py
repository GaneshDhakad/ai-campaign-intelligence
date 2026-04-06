"""
Premium Dark Theme — Glassmorphism SaaS CSS
============================================
Injected into all Streamlit pages for consistent branding.
"""

DARK_THEME_CSS = """
<style>
    /* ── Import Premium Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary: #0a0a1a;
        --bg-secondary: #0f0f23;
        --bg-card: rgba(255, 255, 255, 0.03);
        --bg-card-hover: rgba(255, 255, 255, 0.06);
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.08);
        --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        --text-primary: #e8e8f0;
        --text-secondary: #8b8ba7;
        --text-muted: #5a5a7a;
        --accent-blue: #6366f1;
        --accent-purple: #8b5cf6;
        --accent-cyan: #06b6d4;
        --accent-green: #10b981;
        --accent-amber: #f59e0b;
        --accent-red: #ef4444;
        --gradient-primary: linear-gradient(135deg, #6366f1, #8b5cf6);
        --gradient-success: linear-gradient(135deg, #10b981, #06b6d4);
        --gradient-danger: linear-gradient(135deg, #ef4444, #f59e0b);
        --border-radius: 16px;
        --border-radius-sm: 10px;
    }

    /* ── Global Reset ── */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary) !important;
    }

    /* ── Main Content Area ── */
    .main .block-container {
        max-width: 1400px;
        padding: 2rem 3rem;
    }

    /* ── Headers ── */
    h1, h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    h1 { font-size: 2.2rem !important; }
    h2 { font-size: 1.6rem !important; }
    h3 { font-size: 1.2rem !important; }

    /* ── Glass Card ── */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: var(--glass-shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
        background: var(--bg-card-hover);
        border-color: rgba(99, 102, 241, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15);
    }

    /* ── KPI Card ── */
    .kpi-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: var(--border-radius);
        padding: 1.2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
    }
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .kpi-delta {
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }
    .kpi-delta.positive { color: var(--accent-green); }
    .kpi-delta.negative { color: var(--accent-red); }

    /* ── Color Accent Cards ── */
    .kpi-card.blue::before { background: linear-gradient(135deg, #6366f1, #818cf8); }
    .kpi-card.green::before { background: linear-gradient(135deg, #10b981, #34d399); }
    .kpi-card.amber::before { background: linear-gradient(135deg, #f59e0b, #fbbf24); }
    .kpi-card.red::before { background: linear-gradient(135deg, #ef4444, #f87171); }
    .kpi-card.cyan::before { background: linear-gradient(135deg, #06b6d4, #22d3ee); }
    .kpi-card.purple::before { background: linear-gradient(135deg, #8b5cf6, #a78bfa); }

    /* ── Sentiment Badge ── */
    .sentiment-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .sentiment-positive { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .sentiment-neutral  { background: rgba(139, 139, 167, 0.15); color: #a1a1c7; border: 1px solid rgba(139, 139, 167, 0.3); }
    .sentiment-negative { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

    /* ── Recommendation Box ── */
    .rec-box {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: var(--border-radius);
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
    }
    .rec-box.high { border-left: 4px solid var(--accent-green); }
    .rec-box.medium { border-left: 4px solid var(--accent-amber); }
    .rec-box.low { border-left: 4px solid var(--accent-red); }
    .rec-box h4 {
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .rec-box p {
        margin: 0;
        font-size: 1.05rem;
        color: var(--text-primary);
        line-height: 1.5;
    }

    /* ── Streamlit Overrides ── */
    .stMetric { background: transparent !important; }
    .stMetric label { color: var(--text-secondary) !important; }
    .stMetric [data-testid="stMetricValue"] { color: var(--text-primary) !important; }

    div[data-testid="stExpander"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--border-radius-sm) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border-radius: var(--border-radius-sm);
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: var(--glass-bg) !important;
        color: var(--text-primary) !important;
    }

    /* ── Buttons ── */
    .stButton > button[kind="primary"] {
        background: var(--gradient-primary) !important;
        border: none !important;
        border-radius: var(--border-radius-sm) !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
        padding: 0.7rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
    }

    /* Input fields */
    .stNumberInput input, .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 3px; }

    /* ── Hero Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-banner h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #818cf8, #c084fc, #f0abfc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-banner p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        max-width: 600px;
        margin: 0 auto;
    }

    /* ── Divider ── */
    hr {
        border: none;
        height: 1px;
        background: var(--glass-border);
        margin: 1.5rem 0;
    }

    /* ── Animation ── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeInUp 0.6s ease forwards;
    }

    /* ── Footer ── */
    .engine-footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.8rem;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid var(--glass-border);
        margin-top: 3rem;
    }
    .engine-footer a { color: var(--accent-blue); text-decoration: none; }
</style>
"""


def inject_theme():
    """Inject the dark theme CSS into the current Streamlit page."""
    import streamlit as st
    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)


# Plotly dark template
PLOTLY_DARK_TEMPLATE = {
    'layout': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': '#e8e8f0', 'family': 'Inter'},
        'xaxis': {'gridcolor': 'rgba(255,255,255,0.06)', 'zerolinecolor': 'rgba(255,255,255,0.06)'},
        'yaxis': {'gridcolor': 'rgba(255,255,255,0.06)', 'zerolinecolor': 'rgba(255,255,255,0.06)'},
        'colorway': ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'],
        'margin': {'l': 40, 'r': 20, 't': 40, 'b': 40}
    }
}
