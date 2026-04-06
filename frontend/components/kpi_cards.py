"""
Premium KPI Cards — HTML components for the dashboard
"""

def kpi_card(label: str, value: str, delta: str = "", color: str = "blue", icon: str = "") -> str:
    """Generate a glassmorphism KPI card."""
    delta_class = "positive" if delta and not delta.startswith("-") else "negative"
    delta_html = f'<div class="kpi-delta {delta_class}">{delta}</div>' if delta else ''
    icon_html = f'<span style="font-size:1.5rem; margin-bottom:0.3rem; display:block;">{icon}</span>' if icon else ''

    return f"""
    <div class="kpi-card {color}">
        {icon_html}
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """


def recommendation_box(text: str, level: str = "medium") -> str:
    """Generate a recommendation box."""
    level_map = {"high": "high", "medium": "medium", "low": "low", "very_low": "low"}
    css_class = level_map.get(level.lower().replace(" ", "_"), "medium")

    return f"""
    <div class="rec-box {css_class}">
        <h4>📋 Business Recommendation</h4>
        <p>{text}</p>
    </div>
    """


def sentiment_badge(label: str, compound: float) -> str:
    """Generate a sentiment badge."""
    if label == "Positive" or compound > 0.05:
        css = "sentiment-positive"
        emoji = "😊"
    elif label == "Negative" or compound < -0.05:
        css = "sentiment-negative"
        emoji = "😟"
    else:
        css = "sentiment-neutral"
        emoji = "😐"

    return f'<span class="sentiment-badge {css}">{emoji} {label} ({compound:+.2f})</span>'


def hero_banner(title: str, subtitle: str) -> str:
    """Generate the hero banner."""
    return f"""
    <div class="hero-banner animate-in">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """


def section_header(title: str, subtitle: str = "") -> str:
    """Generate a section header with optional subtitle."""
    sub = f'<p style="color: var(--text-secondary); margin-top: 0.2rem; font-size: 0.9rem;">{subtitle}</p>' if subtitle else ''
    return f"""
    <div style="margin: 1.5rem 0 1rem 0;">
        <h3 style="margin: 0;">{title}</h3>
        {sub}
    </div>
    """


def stat_row(items: list) -> str:
    """Generate a row of stats. items: [(label, value, color), ...]"""
    cols = ""
    for label, value, color in items:
        cols += f"""
        <div style="flex: 1; text-align: center; padding: 0.5rem;">
            <div style="font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;">{label}</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: {color};">{value}</div>
        </div>
        """
    return f'<div style="display: flex; gap: 0.5rem;">{cols}</div>'
