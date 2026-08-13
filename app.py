import streamlit as st

st.set_page_config(page_title="Harsh Vardhan Singh | Analytics Portfolio", page_icon="⚡", layout="wide")

PORTFOLIO_NAME = "Harsh Vardhan Singh"
PORTFOLIO_HEADLINE = "Analytics Portfolio"
PORTFOLIO_BIO = (
    "I build business-focused dashboards that turn raw datasets into clear, decision-ready insights. "
    "This portfolio brings together production-style Streamlit apps with polished UX, practical KPIs, "
    "3D visual exploration, and executive storytelling."
)


if "app_theme" not in st.session_state:
    st.session_state["app_theme"] = "dark"


def get_theme_mode():
    return st.session_state.get("app_theme", "dark")


def get_theme_colors():
    if get_theme_mode() == "light":
        return {
            "mode": "light",
            "app_bg": "radial-gradient(circle at 18% 10%, rgba(14,116,144,0.16), transparent 28rem), radial-gradient(circle at 88% 4%, rgba(180,83,9,0.14), transparent 26rem), linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 48%, #F1F5F9 100%)",
            "sidebar_bg": "linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%)",
            "heading": "#0A0E27",
            "body": "#111827",
            "sub": "#526071",
            "panel": "rgba(255,255,255,0.86)",
            "panel_solid": "#FFFFFF",
            "line": "rgba(15,23,42,0.13)",
            "chip_bg": "rgba(14,116,144,0.08)",
            "chip_text": "#164E63",
            "accent": "#0E7490",
            "accent_2": "#B45309",
            "accent_3": "#1D4ED8",
            "console_bg": "#101827",
            "console_text": "#DDF8FF",
            "shadow": "0 22px 70px rgba(15, 23, 42, 0.12)",
        }
    return {
        "mode": "dark",
        "app_bg": "radial-gradient(circle at 16% 12%, rgba(45,212,191,0.16), transparent 30rem), radial-gradient(circle at 92% 6%, rgba(245,158,11,0.16), transparent 25rem), linear-gradient(135deg, #070B12 0%, #0B1220 50%, #111827 100%)",
        "sidebar_bg": "linear-gradient(180deg, #070B12 0%, #0B1220 100%)",
        "heading": "#F8FAFC",
        "body": "#E5E7EB",
        "sub": "#A7B0C0",
        "panel": "rgba(17,24,39,0.78)",
        "panel_solid": "#101827",
        "line": "rgba(248,250,252,0.14)",
        "chip_bg": "rgba(45,212,191,0.11)",
        "chip_text": "#DDFCF7",
        "accent": "#2DD4BF",
        "accent_2": "#F59E0B",
        "accent_3": "#60A5FA",
        "console_bg": "#050A12",
        "console_text": "#BEFFF7",
        "shadow": "0 26px 84px rgba(0, 0, 0, 0.38)",
    }


def theme_toggle():
    st.sidebar.markdown("---")
    st.sidebar.write("**Theme**")
    options = ["Light", "Dark"]
    current = "Light" if get_theme_mode() == "light" else "Dark"
    selected = st.sidebar.radio("Select theme", options=options, index=options.index(current), label_visibility="collapsed")
    new_theme = "light" if selected == "Light" else "dark"
    if st.session_state.get("app_theme") != new_theme:
        st.session_state["app_theme"] = new_theme
        st.rerun()


def inject_styles():
    c = get_theme_colors()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {c['app_bg']};
            color: {c['body']};
        }}
        [data-testid="stHeader"] {{
            background: transparent;
        }}
        [data-testid="stSidebar"] {{
            background: {c['sidebar_bg']};
            border-right: 1px solid {c['line']};
        }}
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebarNav"] span,
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNavItems"] span,
        [data-testid="stSidebarNavItems"] a,
        [data-testid="stSidebarNavLink"] span,
        [data-testid="stSidebarContent"] p,
        [data-testid="stSidebarContent"] span {{
            color: {c['body']} !important;
        }}
        .block-container {{
            max-width: 1280px;
            padding-top: 2.1rem;
            padding-bottom: 3.2rem;
        }}
        .pf-sidebar-brand {{
            display: flex;
            gap: 0.85rem;
            align-items: center;
            padding: 0.35rem 0 1.15rem;
            border-bottom: 1px solid {c['line']};
        }}
        .pf-brand-mark {{
            width: 46px;
            height: 46px;
            display: grid;
            place-items: center;
            border-radius: 14px;
            color: #06100F;
            background: linear-gradient(135deg, {c['accent']}, {c['accent_2']});
            font-weight: 900;
            box-shadow: {c['shadow']};
        }}
        .pf-brand-name {{
            color: {c['heading']};
            font-weight: 850;
            line-height: 1.05;
        }}
        .pf-brand-sub {{
            color: {c['sub']};
            font-size: 0.78rem;
            margin-top: 0.16rem;
        }}
        .pf-sidebar-note {{
            margin-top: 1.25rem;
            padding: 0.95rem;
            border: 1px solid {c['line']};
            border-radius: 14px;
            background: {c['chip_bg']};
            color: {c['sub']};
            font-size: 0.82rem;
            line-height: 1.5;
        }}
        .pf-sidebar-note strong {{
            color: {c['heading']};
            display: block;
            margin-bottom: 0.35rem;
        }}
        .pf-hero {{
            position: relative;
            overflow: hidden;
            border: 1px solid {c['line']};
            border-radius: 28px;
            background: linear-gradient(135deg, {c['panel']}, {c['panel_solid']});
            box-shadow: {c['shadow']};
            padding: clamp(2rem, 5vw, 4.6rem);
        }}
        .pf-hero:after {{
            content: "";
            position: absolute;
            right: -8%;
            bottom: -30%;
            width: 58%;
            height: 280px;
            background: linear-gradient(90deg, {c['accent']}, {c['accent_2']}, {c['accent_3']});
            filter: blur(42px);
            opacity: 0.24;
            transform: rotate(-8deg);
        }}
        .pf-hero-grid {{
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
            gap: clamp(1.4rem, 4vw, 3rem);
            align-items: center;
        }}
        .pf-eyebrow {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.45rem 0.75rem;
            border: 1px solid {c['line']};
            border-radius: 999px;
            background: {c['chip_bg']};
            color: {c['accent']};
            font-size: 0.78rem;
            font-weight: 850;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}
        .pf-title {{
            margin: 1.1rem 0 0.2rem;
            color: {c['heading']};
            font-size: clamp(2.75rem, 5.6vw, 5.7rem);
            line-height: 0.94;
            font-weight: 950;
            letter-spacing: -0.04em;
        }}
        .pf-title-line {{
            display: block;
            white-space: nowrap;
        }}
        .pf-title span {{
            color: {c['accent']};
        }}
        .pf-headline {{
            margin-top: 0.6rem;
            color: {c['accent_2']};
            font-size: clamp(1.1rem, 2vw, 1.55rem);
            font-weight: 850;
        }}
        .pf-bio {{
            max-width: 720px;
            color: {c['sub']};
            font-size: 1.04rem;
            line-height: 1.72;
            margin-top: 1.05rem;
        }}
        .pf-pill-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            margin-top: 1.55rem;
        }}
        .pf-pill {{
            padding: 0.6rem 0.85rem;
            border: 1px solid {c['line']};
            border-radius: 999px;
            background: {c['chip_bg']};
            color: {c['chip_text']};
            font-size: 0.86rem;
            font-weight: 750;
        }}
        .pf-console {{
            border: 1px solid {c['line']};
            border-radius: 22px;
            background: {c['console_bg']};
            box-shadow: {c['shadow']};
            overflow: hidden;
        }}
        .pf-console-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.9rem 1rem;
            color: {c['console_text']};
            border-bottom: 1px solid rgba(255,255,255,0.12);
            font-size: 0.82rem;
            font-weight: 800;
        }}
        .pf-lights {{
            display: flex;
            gap: 0.42rem;
        }}
        .pf-light {{
            width: 10px;
            height: 10px;
            border-radius: 999px;
        }}
        .pf-red {{ background: #FB7185; }}
        .pf-yellow {{ background: #FBBF24; }}
        .pf-green {{ background: #34D399; }}
        .pf-console-body {{
            padding: 1.1rem;
            color: {c['console_text']};
            font-family: Consolas, monospace;
            font-size: 0.86rem;
            line-height: 1.75;
        }}
        .pf-console-line {{
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.44rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }}
        .pf-console-key {{
            color: #7DD3FC;
        }}
        .pf-console-val {{
            text-align: right;
            color: #F8FAFC;
        }}
        .pf-console-good {{
            color: #5EEAD4;
        }}
        .pf-stats {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 1rem;
            margin: 1.15rem 0 1.9rem;
        }}
        .pf-stat {{
            border: 1px solid {c['line']};
            border-radius: 18px;
            background: {c['panel']};
            padding: 1rem;
            box-shadow: {c['shadow']};
        }}
        .pf-stat-value {{
            color: {c['heading']};
            font-size: clamp(1.55rem, 3vw, 2.2rem);
            line-height: 1;
            font-weight: 950;
        }}
        .pf-stat-label {{
            color: {c['sub']};
            margin-top: 0.45rem;
            font-size: 0.86rem;
            line-height: 1.4;
        }}
        .pf-section {{
            margin: 2rem 0 1rem;
        }}
        .pf-kicker {{
            color: {c['accent']};
            font-size: 0.76rem;
            text-transform: uppercase;
            font-weight: 900;
            letter-spacing: 0.1em;
        }}
        .pf-section-title {{
            color: {c['heading']};
            font-size: clamp(1.7rem, 3vw, 2.55rem);
            font-weight: 950;
            margin-top: 0.25rem;
            letter-spacing: -0.03em;
        }}
        .pf-card {{
            min-height: 325px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 1.2rem;
            border: 1px solid {c['line']};
            border-radius: 22px;
            background: linear-gradient(180deg, {c['panel_solid']}, {c['panel']});
            box-shadow: {c['shadow']};
            position: relative;
            overflow: hidden;
        }}
        .pf-card:after {{
            content: "";
            position: absolute;
            top: 1rem;
            right: 1rem;
            width: 88px;
            height: 88px;
            border-radius: 24px;
            background: var(--pf-card-color);
            opacity: 0.14;
            transform: rotate(12deg);
        }}
        .pf-card-icon {{
            width: 56px;
            height: 56px;
            display: grid;
            place-items: center;
            border: 1px solid {c['line']};
            border-radius: 16px;
            background: color-mix(in srgb, var(--pf-card-color) 18%, transparent);
            font-size: 1.55rem;
        }}
        .pf-card-title {{
            margin-top: 1.1rem;
            color: {c['heading']};
            font-size: 1.35rem;
            font-weight: 950;
        }}
        .pf-card-copy {{
            color: {c['sub']};
            margin-top: 0.55rem;
            line-height: 1.62;
            font-size: 0.95rem;
        }}
        .pf-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 1rem;
        }}
        .pf-tag {{
            color: {c['chip_text']};
            border: 1px solid {c['line']};
            background: {c['chip_bg']};
            border-radius: 999px;
            padding: 0.34rem 0.55rem;
            font-size: 0.75rem;
            font-weight: 760;
        }}
        .pf-note {{
            border: 1px solid {c['line']};
            border-radius: 20px;
            padding: 1rem 1.1rem;
            background: {c['panel']};
            color: {c['sub']};
            line-height: 1.55;
            margin-top: 1.35rem;
        }}
        .pf-note strong {{
            color: {c['heading']};
        }}
        div[data-testid="stPageLink"] a {{
            border: 1px solid {c['line']};
            border-radius: 14px;
            background: {c['panel_solid']};
            color: {c['heading']} !important;
            transition: border-color 160ms ease, transform 160ms ease;
        }}
        div[data-testid="stPageLink"] a *,
        div[data-testid="stPageLink"] span,
        div[data-testid="stPageLink"] p {{
            color: {c['heading']} !important;
            opacity: 1 !important;
        }}
        div[data-testid="stPageLink"] a:hover {{
            border-color: {c['accent']};
            transform: translateY(-1px);
        }}
        @media (max-width: 900px) {{
            .pf-hero-grid {{ grid-template-columns: 1fr; }}
            .pf-stats {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        }}
        @media (max-width: 560px) {{
            .pf-title-line {{ white-space: normal; }}
            .pf-stats {{ grid-template-columns: 1fr; }}
            .pf-card {{ min-height: auto; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_styles()

st.sidebar.markdown(
    f"""
    <div class="pf-sidebar-brand">
      <div class="pf-brand-mark">HVS</div>
      <div>
        <div class="pf-brand-name">{PORTFOLIO_NAME}</div>
        <div class="pf-brand-sub">{PORTFOLIO_HEADLINE}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
theme_toggle()
st.sidebar.markdown(
    """
    <div class="pf-sidebar-note">
      <strong>Portfolio scope</strong>
      Multi-page Streamlit analytics portfolio with commerce, travel, and food-market dashboards.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <section class="pf-hero">
      <div class="pf-hero-grid">
        <div>
          <div class="pf-eyebrow">Portfolio command center</div>
          <div class="pf-title"><span class="pf-title-line">Harsh Vardhan</span><span>Singh</span></div>
          <div class="pf-headline">{PORTFOLIO_HEADLINE}</div>
          <div class="pf-bio">{PORTFOLIO_BIO}</div>
          <div class="pf-pill-row">
            <span class="pf-pill">Streamlit Apps</span>
            <span class="pf-pill">Plotly Visuals</span>
            <span class="pf-pill">3D Exploration</span>
            <span class="pf-pill">Executive KPIs</span>
          </div>
        </div>
        <div class="pf-console">
          <div class="pf-console-top">
            <span>portfolio_console.py</span>
            <span class="pf-lights"><span class="pf-light pf-red"></span><span class="pf-light pf-yellow"></span><span class="pf-light pf-green"></span></span>
          </div>
          <div class="pf-console-body">
            <div class="pf-console-line"><span class="pf-console-key">owner</span><span class="pf-console-val">Harsh Vardhan Singh</span></div>
            <div class="pf-console-line"><span class="pf-console-key">dashboards</span><span class="pf-console-val">commerce · travel · zomato</span></div>
            <div class="pf-console-line"><span class="pf-console-key">visual_layer</span><span class="pf-console-val pf-console-good">2D + 3D analytics</span></div>
            <div class="pf-console-line"><span class="pf-console-key">workflow</span><span class="pf-console-val">upload → mapping → quality → insights</span></div>
            <div class="pf-console-line"><span class="pf-console-key">status</span><span class="pf-console-val pf-console-good">ready for showcase</span></div>
          </div>
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="pf-stats">
      <div class="pf-stat"><div class="pf-stat-value">03</div><div class="pf-stat-label">Interactive dashboard suites</div></div>
      <div class="pf-stat"><div class="pf-stat-value">3D</div><div class="pf-stat-label">Advanced visual exploration layer</div></div>
      <div class="pf-stat"><div class="pf-stat-value">KPI</div><div class="pf-stat-label">Business-first metric storytelling</div></div>
      <div class="pf-stat"><div class="pf-stat-value">BI</div><div class="pf-stat-label">Portfolio-ready analytics workflow</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="pf-section">
      <div class="pf-kicker">Featured work</div>
      <div class="pf-section-title">Choose a dashboard</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        """
        <div class="pf-card" style="--pf-card-color:#2DD4BF;">
          <div>
            <div class="pf-card-icon">🛒</div>
            <div class="pf-card-title">E-commerce Performance</div>
            <div class="pf-card-copy">Premium marketplace analytics with category tile filters, revenue operations, returns, fulfillment, and 3D commerce visuals.</div>
            <div class="pf-tags"><span class="pf-tag">3D Visuals</span><span class="pf-tag">Category Filters</span><span class="pf-tag">Revenue Ops</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_🛒_Ecommerce_Dashboard.py", label="Open E-commerce Dashboard", icon="🛒")

with col2:
    st.markdown(
        """
        <div class="pf-card" style="--pf-card-color:#F59E0B;">
          <div>
            <div class="pf-card-icon">✈️</div>
            <div class="pf-card-title">Travel Analytics</div>
            <div class="pf-card-copy">Pipeline-ready flight behavior and booking trend insights with route demand, fare timing, and 3D fare-space analysis.</div>
            <div class="pf-tags"><span class="pf-tag">Fare Space</span><span class="pf-tag">Route Demand</span><span class="pf-tag">KPI Design</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_✈️_Travel_Dashboard.py", label="Open Travel Dashboard", icon="✈️")

with col3:
    st.markdown(
        """
        <div class="pf-card" style="--pf-card-color:#FB7185;">
          <div>
            <div class="pf-card-icon">🍽️</div>
            <div class="pf-card-title">Zomato Intelligence</div>
            <div class="pf-card-copy">Restaurant market analytics with smart data onboarding, filtering, geospatial views, ratings, and 3D restaurant-space exploration.</div>
            <div class="pf-tags"><span class="pf-tag">Geospatial</span><span class="pf-tag">Cuisine</span><span class="pf-tag">Restaurant KPIs</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_🍽️_Zomato_Dashboard.py", label="Open Zomato Dashboard", icon="📊")

st.markdown(
    """
    <div class="pf-note">
      <strong>Dataset Convention:</strong>
      each project keeps its dataset under <code>data/&lt;project-name&gt;/</code>, making the portfolio easy to scale as new dashboard domains are added.
    </div>
    """,
    unsafe_allow_html=True,
)
