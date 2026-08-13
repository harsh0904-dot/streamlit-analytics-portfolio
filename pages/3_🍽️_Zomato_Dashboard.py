import pathlib
import urllib.parse
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Zomato Dashboard", layout="wide")

THEME_PRIMARY = "#B42318"
THEME_SECONDARY = "#FDA29B"
THEME_DARK = "#7A271A"
THEME_BG = "#F8FAFC"
CHART_HEIGHT = 380


def get_theme_mode():
    """Get current theme from session state (user-selected or default to dark)."""
    if "app_theme" not in st.session_state:
        st.session_state["app_theme"] = "dark"
    return st.session_state["app_theme"]


def theme_toggle(show_brand=False):
    """Render theme toggle in sidebar; brand panel only on source page."""
    if show_brand:
        colors = get_theme_colors()
        panel_bg = "rgba(180,35,24,0.12)" if get_theme_mode() == "dark" else "rgba(180,35,24,0.07)"
        sub_color = colors["sub_color"]
        st.sidebar.markdown(
            f"""
            <div style="background:{panel_bg};border-radius:14px;padding:14px 12px 10px 12px;margin-bottom:10px;border:1px solid rgba(180,35,24,0.22);">
              <div style="text-align:center;margin-bottom:6px;">
                <svg xmlns='http://www.w3.org/2000/svg' width='120' height='38' viewBox='0 0 120 38'>
                  <rect x='1' y='1' width='118' height='36' rx='18' ry='18' fill='#B42318'/>
                  <text x='60' y='25' font-size='19' font-family='Segoe UI,Arial,sans-serif' font-weight='800'
                        fill='#FFFFFF' text-anchor='middle' letter-spacing='-0.5'>zomato</text>
                </svg>
              </div>
              <div style="text-align:center;font-size:0.72rem;color:{sub_color};margin-top:4px;letter-spacing:0.5px;">Food Intelligence Platform</div>
              <div style="display:flex;justify-content:center;gap:10px;margin-top:8px;font-size:1.15rem;">🍛 🛵 📊 📍 ⭐</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.sidebar.markdown("---")
    st.sidebar.write("**Theme**")
    theme_options = ["Light", "Dark"]
    current = "Light" if get_theme_mode() == "light" else "Dark"
    selected = st.sidebar.radio("Select theme", options=theme_options, index=theme_options.index(current), label_visibility="collapsed")
    new_theme = "light" if selected == "Light" else "dark"
    if st.session_state.get("app_theme") != new_theme:
        st.session_state["app_theme"] = new_theme
        st.rerun()


def get_theme_colors():
    """Returns all theme-dependent colors. Called on every rerun to detect theme changes."""
    theme_mode = get_theme_mode()
    if theme_mode == "light":
        return {
            "mode": "light",
            "chart_plot_bg": "#FFFFFF",
            "chart_paper_bg": "#F8FAFC",
            "chart_font": "#0A0E27",
            "chart_grid": "#CBD5E1",
            "chart_tick": "#1E293B",
            "heading_color": "#0A0E27",
            "subtitle_color": "#334155",
            "body_color": "#0A0E27",
            "sidebar_bg": "#F1F5F9",
            "app_bg": "linear-gradient(180deg, #f8fafc 0%, #ffffff 50%, #f1f5f9 100%)",
            "card_bg": "#FFFFFF",
            "card_border": "#CBD5E1",
            "feature_bg": "#F8FAFC",
            "feature_text": "#0A0E27",
            "step_bg": "#FFFFFF",
            "step_color": "#1E293B",
            "metric_bg": "#FFFFFF",
            "metric_label": "#1E293B",
            "metric_value": "#0A0E27",
            "desc_color": "#334155",
            "sub_color": "#475569",
        }
    else:
        return {
            "mode": "dark",
            "chart_plot_bg": "#111827",
            "chart_paper_bg": "#0f172a",
            "chart_font": "#F9FAFB",
            "chart_grid": "#374151",
            "chart_tick": "#E5E7EB",
            "heading_color": "#F9FAFB",
            "subtitle_color": "#D1D5DB",
            "body_color": "#E5E7EB",
            "sidebar_bg": "#0b1220",
            "app_bg": "linear-gradient(180deg, #0b1020 0%, #111827 50%, #0f172a 100%)",
            "card_bg": "#111827",
            "card_border": "#374151",
            "feature_bg": "#0f172a",
            "feature_text": "#E5E7EB",
            "step_bg": "#111827",
            "step_color": "#D1D5DB",
            "metric_bg": "#111827",
            "metric_label": "#D1D5DB",
            "metric_value": "#F9FAFB",
            "desc_color": "#D1D5DB",
            "sub_color": "#9CA3AF",
        }


def inject_styles():
    colors = get_theme_colors()
    theme_mode = get_theme_mode()
    heading_color = colors["heading_color"]
    subtitle_color = colors["subtitle_color"]
    body_color = colors["body_color"]
    sidebar_bg = colors["sidebar_bg"]
    app_bg = colors["app_bg"]
    card_bg = colors["card_bg"]
    card_border = colors["card_border"]
    feature_bg = colors["feature_bg"]
    feature_text = colors["feature_text"]
    step_bg = colors["step_bg"]
    step_color = colors["step_color"]
    metric_bg = colors["metric_bg"]
    metric_label = colors["metric_label"]
    metric_value = colors["metric_value"]

    # Only apply white text to dark form elements in light theme
    form_elements_css = ""
    if theme_mode == "light":
        form_elements_css = f"""
        input::placeholder {{
            color: #AAAAAA !important;
            opacity: 1 !important;
        }}
        input, input[type="text"], input[type="email"], input[type="password"], input[type="number"] {{
            color: #FFFFFF !important;
        }}
        textarea {{
            color: #FFFFFF !important;
        }}
        textarea::placeholder {{
            color: #AAAAAA !important;
            opacity: 1 !important;
        }}
        select, select option {{
            color: #FFFFFF !important;
        }}
        [data-testid="stFileUploader"] * {{
            color: #FFFFFF !important;
        }}
        button, button * {{
            color: #FFFFFF !important;
        }}
        [data-testid="stButton"] button, [data-testid="stButton"] button * {{
            color: #FFFFFF !important;
        }}
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary *,
        [data-testid="stExpander"] details summary,
        [data-testid="stExpander"] [role="button"],
        .streamlit-expanderHeader,
        .streamlit-expanderHeader * {{
            color: #FFFFFF !important;
        }}
        [data-testid="stSelectbox"] *,
        [data-testid="stMultiSelect"] *,
        [data-testid="stSlider"] label,
        [data-testid="stSlider"] span,
        [data-testid="stCheckbox"] label,
        [data-testid="stCheckbox"] span {{
            color: #FFFFFF !important;
        }}
        [data-testid="stSidebarNav"] span,
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNavItems"] span,
        [data-testid="stSidebarNavItems"] a,
        [data-testid="stSidebarNavLink"] span {{
            color: {body_color} !important;
        }}
        """
    watermark_html = ""

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {app_bg};
            color: {body_color};
        }}
        [data-testid="stHeader"] {{
            background: transparent;
        }}
        [data-testid="stSidebar"] {{
            background: {sidebar_bg};
        }}
        .block-container {{
            padding-top: 2.2rem;
            padding-bottom: 1.2rem;
        }}
        .main-title {{
            line-height: 1.25 !important;
            margin-top: 0.2rem !important;
            margin-bottom: 0.15rem !important;
            color: {heading_color} !important;
            font-size: 2.45rem !important;
            font-weight: 800 !important;
        }}
        .section-title {{
            font-size: 1.25rem;
            font-weight: 700;
            margin-top: 0.25rem;
            margin-bottom: 0.5rem;
            color: {heading_color};
        }}
        .section-subtitle {{
            color: {subtitle_color};
            margin-top: -0.25rem;
            margin-bottom: 0.75rem;
        }}
        .landing-card {{
            border: 1px solid {card_border};
            border-radius: 16px;
            background: {card_bg};
            padding: 18px 20px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.25);
        }}
        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin-top: 8px;
        }}
        .feature-item {{
            border: 1px solid {card_border};
            border-radius: 12px;
            padding: 10px 12px;
            background: {feature_bg};
            color: {feature_text};
        }}
        .stepper {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
            margin: 12px 0 4px 0;
        }}
        .step {{
            padding: 8px 10px;
            border-radius: 999px;
            font-size: 0.85rem;
            text-align: center;
            border: 1px solid {card_border};
            color: {step_color};
            background: {step_bg};
        }}
        .step.active {{
            border-color: #b42318;
            color: #FECACA;
            background: #7f1d1d;
            font-weight: 700;
        }}

        /* Critical readability fixes: labels and values must stay visible */
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stCaptionContainer"],
        [data-testid="stText"],
        label,
        .st-emotion-cache-16idsys p {{
            color: {body_color} !important;
        }}

        {form_elements_css}

        [data-testid="stMetric"] {{
            background: {metric_bg};
            border: 1px solid {card_border};
            border-radius: 12px;
            padding: 10px 12px;
        }}

        [data-testid="stMetricLabel"] p {{
            color: {metric_label} !important;
            font-weight: 600 !important;
        }}

        [data-testid="stMetricValue"] div {{
            color: {metric_value} !important;
            font-weight: 700 !important;
        }}

        [data-testid="stDataFrame"] {{
            border: 1px solid {card_border};
            border-radius: 10px;
            overflow: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_stepper(active_step):
    labels = ["1. Source", "2. Mapping", "3. Quality Check", "4. Dashboard"]
    html = '<div class="stepper">'
    for idx, label in enumerate(labels, start=1):
        active_cls = " active" if idx == active_step else ""
        html += f'<div class="step{active_cls}">{label}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def build_demo_dataset(rows=1200):
    rng = np.random.default_rng(42)
    cities = ["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad", "Chennai", "Kolkata", "Jaipur"]
    cuisines = ["North Indian", "South Indian", "Chinese", "Fast Food", "Cafe", "Desserts", "Continental", "Beverages"]
    city_latlon = {
        "Mumbai": (19.0760, 72.8777),
        "Delhi": (28.7041, 77.1025),
        "Bangalore": (12.9716, 77.5946),
        "Pune": (18.5204, 73.8567),
        "Hyderabad": (17.3850, 78.4867),
        "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639),
        "Jaipur": (26.9124, 75.7873),
    }

    chosen_cities = rng.choice(cities, size=rows, replace=True)
    chosen_cuisines = rng.choice(cuisines, size=rows, replace=True)
    ratings = np.clip(rng.normal(3.4, 0.8, size=rows), 1.0, 5.0)
    cost = np.clip(rng.normal(700, 320, size=rows), 120, 3000)
    votes = np.clip(rng.lognormal(mean=4.6, sigma=0.9, size=rows), 1, 12000)

    lat = []
    lon = []
    for c in chosen_cities:
        base_lat, base_lon = city_latlon[c]
        lat.append(base_lat + rng.normal(0, 0.08))
        lon.append(base_lon + rng.normal(0, 0.08))

    df_demo = pd.DataFrame(
        {
            "restaurant_name": [f"Restaurant {i+1}" for i in range(rows)],
            "city": chosen_cities,
            "cuisines": chosen_cuisines,
            "aggregate_rating": np.round(ratings, 2),
            "average_cost_for_two": np.round(cost).astype(int),
            "votes": np.round(votes).astype(int),
            "latitude": np.round(lat, 6),
            "longitude": np.round(lon, 6),
        }
    )
    return df_demo


def normalize_col_name(col):
    return str(col).strip().lower().replace("_", " ").replace("-", " ")


def find_column(columns, candidate_keywords):
    normalized = {col: normalize_col_name(col) for col in columns}
    for col, norm in normalized.items():
        for key in candidate_keywords:
            if key in norm:
                return col
    return None


def to_numeric_series(s):
    return pd.to_numeric(s.astype(str).str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")


def minmax(s):
    s = pd.to_numeric(s, errors="coerce")
    if s.notna().sum() == 0:
        return pd.Series([0] * len(s), index=s.index)
    mn, mx = s.min(), s.max()
    if pd.isna(mn) or pd.isna(mx) or mn == mx:
        return pd.Series([0] * len(s), index=s.index)
    return (s - mn) / (mx - mn)


def style_figure(fig, title):
    colors = get_theme_colors()
    fig.update_layout(
        title=title,
        plot_bgcolor=colors["chart_plot_bg"],
        paper_bgcolor=colors["chart_paper_bg"],
        font=dict(color=colors["chart_font"]),
        margin=dict(l=10, r=10, t=55, b=20),
        height=CHART_HEIGHT,
        title_font=dict(size=18, color=colors["chart_font"]),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=colors["chart_font"]),
        ),
        uniformtext_minsize=10,
        uniformtext_mode="hide",
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=colors["chart_grid"],
        tickfont=dict(color=colors["chart_tick"]),
        title_font=dict(color=colors["chart_font"]),
        automargin=True,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=colors["chart_grid"],
        tickfont=dict(color=colors["chart_tick"]),
        title_font=dict(color=colors["chart_font"]),
        automargin=True,
    )
    return fig


def load_dataset(uploaded):
    ext = pathlib.Path(uploaded.name).suffix.lower()
    try:
        if ext in {".xlsx", ".xls"}:
            uploaded.seek(0)
            return pd.read_excel(uploaded), None
        if ext == ".csv":
            for enc in ["utf-8", "utf-8-sig", "latin-1"]:
                try:
                    uploaded.seek(0)
                    return pd.read_csv(uploaded, sep=None, engine="python", encoding=enc), None
                except Exception:
                    continue
            return None, "Could not read CSV with supported encodings."
        if ext == ".tsv":
            uploaded.seek(0)
            return pd.read_csv(uploaded, sep="\t"), None
        if ext == ".json":
            uploaded.seek(0)
            return pd.read_json(uploaded), None
        if ext == ".parquet":
            uploaded.seek(0)
            return pd.read_parquet(uploaded), None
        return None, "Unsupported file format. Use CSV, XLSX, XLS, TSV, JSON, or Parquet."
    except Exception as ex:
        return None, f"Failed to parse file: {ex}"


def clean_with_mapping(raw_df, mapping):
    df_clean = raw_df.copy()

    for col in df_clean.columns:
        if df_clean[col].dtype == "object":
            df_clean[col] = df_clean[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    rating_col = mapping.get("rating")
    cost_col = mapping.get("cost")
    votes_col = mapping.get("votes")
    lat_col = mapping.get("latitude")
    lon_col = mapping.get("longitude")

    if rating_col:
        df_clean[rating_col] = to_numeric_series(df_clean[rating_col]).clip(lower=0, upper=5)
    if cost_col:
        df_clean[cost_col] = to_numeric_series(df_clean[cost_col]).clip(lower=0)
    if votes_col:
        df_clean[votes_col] = to_numeric_series(df_clean[votes_col]).clip(lower=0)
    if lat_col:
        df_clean[lat_col] = to_numeric_series(df_clean[lat_col])
    if lon_col:
        df_clean[lon_col] = to_numeric_series(df_clean[lon_col])

    if lat_col and lon_col:
        valid_geo = (
            df_clean[lat_col].between(-90, 90, inclusive="both")
            & df_clean[lon_col].between(-180, 180, inclusive="both")
        )
        df_clean.loc[~valid_geo, [lat_col, lon_col]] = np.nan

    return df_clean


def render_landing():
    colors = get_theme_colors()
    heading_color = colors["heading_color"]
    desc_color = colors["desc_color"]
    sub_color = colors["sub_color"]
    card_bg = colors["card_bg"]
    card_border = colors["card_border"]
    feature_bg = colors["feature_bg"]
    mode = get_theme_mode()
    hero_bg = "rgba(180,35,24,0.10)" if mode == "dark" else "rgba(180,35,24,0.06)"
    icon_bg = "rgba(180,35,24,0.15)" if mode == "dark" else "rgba(180,35,24,0.08)"

    # Two-column hero: title left, SVG collage right
    col_title, col_hero = st.columns([3, 2], gap="large")
    with col_title:
        st.markdown('<h1 class="main-title">Zomato Intelligence Dashboard</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:{desc_color};font-size:1.05rem;margin-top:0.2rem;margin-bottom:1rem;">Upload any data format, auto-clean it, map columns — and generate portfolio-grade restaurant insights.</p>', unsafe_allow_html=True)
        # Stats strip
        st.markdown(
            f"""
            <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:1rem;">
              <div style="background:{icon_bg};border-radius:10px;padding:8px 14px;text-align:center;">
                <div style="font-size:1.3rem;font-weight:800;color:#B42318;">8+</div>
                <div style="font-size:0.72rem;color:{sub_color};">Cities</div>
              </div>
              <div style="background:{icon_bg};border-radius:10px;padding:8px 14px;text-align:center;">
                <div style="font-size:1.3rem;font-weight:800;color:#B42318;">1200+</div>
                <div style="font-size:0.72rem;color:{sub_color};">Restaurants</div>
              </div>
              <div style="background:{icon_bg};border-radius:10px;padding:8px 14px;text-align:center;">
                <div style="font-size:1.3rem;font-weight:800;color:#B42318;">6</div>
                <div style="font-size:0.72rem;color:{sub_color};">File Formats</div>
              </div>
              <div style="background:{icon_bg};border-radius:10px;padding:8px 14px;text-align:center;">
                <div style="font-size:1.3rem;font-weight:800;color:#B42318;">4</div>
                <div style="font-size:0.72rem;color:{sub_color};">Dashboard Tabs</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_hero:
        # Inline SVG: food bowl + delivery bike + chart icon collage
        st.markdown(
            f"""
            <div style="background:{hero_bg};border-radius:20px;padding:18px 10px;border:1px solid rgba(180,35,24,0.18);height:100%;min-height:160px;display:flex;align-items:center;justify-content:center;">
              <svg xmlns='http://www.w3.org/2000/svg' width='320' height='160' viewBox='0 0 320 160'>
                <!-- Food bowl -->
                <ellipse cx='62' cy='105' rx='40' ry='14' fill='rgba(180,35,24,0.18)'/>
                <path d='M28 90 Q30 60 62 58 Q94 60 96 90 Z' fill='#B42318' opacity='0.85'/>
                <ellipse cx='62' cy='90' rx='34' ry='8' fill='#FDA29B' opacity='0.6'/>
                <circle cx='52' cy='80' r='5' fill='#7A271A' opacity='0.7'/>
                <circle cx='65' cy='76' r='4' fill='#B42318' opacity='0.6'/>
                <circle cx='76' cy='82' r='5' fill='#7A271A' opacity='0.7'/>
                <!-- Steam lines -->
                <path d='M50 55 Q47 48 50 42' stroke='#FDA29B' stroke-width='2' fill='none' stroke-linecap='round' opacity='0.6'/>
                <path d='M62 52 Q59 45 62 38' stroke='#FDA29B' stroke-width='2' fill='none' stroke-linecap='round' opacity='0.6'/>
                <path d='M74 55 Q71 48 74 42' stroke='#FDA29B' stroke-width='2' fill='none' stroke-linecap='round' opacity='0.6'/>
                <!-- Delivery bike -->
                <circle cx='188' cy='108' r='16' fill='none' stroke='#B42318' stroke-width='3' opacity='0.8'/>
                <circle cx='188' cy='108' r='4' fill='#B42318' opacity='0.8'/>
                <circle cx='240' cy='108' r='16' fill='none' stroke='#B42318' stroke-width='3' opacity='0.8'/>
                <circle cx='240' cy='108' r='4' fill='#B42318' opacity='0.8'/>
                <path d='M188 108 L200 88 L228 88 L240 108' stroke='#7A271A' stroke-width='3' fill='none' stroke-linejoin='round' opacity='0.9'/>
                <path d='M200 88 L205 72 L225 72 L228 88' fill='#B42318' opacity='0.75'/>
                <circle cx='205' cy='72' r='5' fill='#FDA29B' opacity='0.8'/>
                <!-- Delivery box on rider -->
                <rect x='213' y='60' width='22' height='16' rx='3' fill='#B42318' opacity='0.7'/>
                <text x='224' y='72' font-size='8' font-family='Arial' font-weight='700' fill='white' text-anchor='middle' opacity='0.9'>Z</text>
                <!-- Bar chart -->
                <rect x='272' y='100' width='10' height='30' rx='2' fill='#B42318' opacity='0.8'/>
                <rect x='286' y='82' width='10' height='48' rx='2' fill='#FDA29B' opacity='0.8'/>
                <rect x='300' y='90' width='10' height='40' rx='2' fill='#7A271A' opacity='0.8'/>
                <line x1='268' y1='130' x2='315' y2='130' stroke='#B42318' stroke-width='2' opacity='0.5'/>
                <!-- Map pin -->
                <circle cx='155' cy='50' r='10' fill='#B42318' opacity='0.85'/>
                <path d='M155 60 L150 75 L155 70 L160 75 Z' fill='#B42318' opacity='0.85'/>
                <circle cx='155' cy='50' r='4' fill='white' opacity='0.9'/>
                <!-- Stars -->
                <text x='130' y='120' font-size='13' fill='#FDA29B' opacity='0.7'>★★★★★</text>
              </svg>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Feature cards with icons
    st.markdown(
        f"""
        <div class="landing-card" style="margin-top:14px;">
            <h3 style="margin:0 0 10px 0;color:{heading_color};">Professional Data Onboarding</h3>
            <p style="margin:0 0 12px 0;color:{desc_color};">Handles messy real-world files — auto-detects formats, cleans numeric fields, validates geo coordinates, and guides you step-by-step.</p>
            <div class="feature-grid">
                <div class="feature-item">
                  <div style="font-size:1.6rem;margin-bottom:6px;">📂</div>
                  <strong style="color:{heading_color};">Multi-format Upload</strong><br>
                  <span style="color:{sub_color};font-size:0.85rem;">CSV, Excel, TSV, JSON, Parquet — with encoding fallbacks</span>
                </div>
                <div class="feature-item">
                  <div style="font-size:1.6rem;margin-bottom:6px;">⚡</div>
                  <strong style="color:{heading_color};">Auto-cleaning</strong><br>
                  <span style="color:{sub_color};font-size:0.85rem;">Numeric fixes, null handling, geo coordinate validation</span>
                </div>
                <div class="feature-item">
                  <div style="font-size:1.6rem;margin-bottom:6px;">🗺️</div>
                  <strong style="color:{heading_color};">Smart Column Mapping</strong><br>
                  <span style="color:{sub_color};font-size:0.85rem;">Flexible schema — no hardcoded field names required</span>
                </div>
                <div class="feature-item">
                  <div style="font-size:1.6rem;margin-bottom:6px;">📊</div>
                  <strong style="color:{heading_color};">4 Dashboard Tabs</strong><br>
                  <span style="color:{sub_color};font-size:0.85rem;">Overview, Cuisine, Geo map, and Data export</span>
                </div>
                <div class="feature-item">
                  <div style="font-size:1.6rem;margin-bottom:6px;">⭐</div>
                  <strong style="color:{heading_color};">Weighted Ratings</strong><br>
                  <span style="color:{sub_color};font-size:0.85rem;">Vote-weighted scores and opportunity scoring per city</span>
                </div>
                <div class="feature-item">
                  <div style="font-size:1.6rem;margin-bottom:6px;">🌙 / ☀️</div>
                  <strong style="color:{heading_color};">Dark & Light Theme</strong><br>
                  <span style="color:{sub_color};font-size:0.85rem;">Switch anytime from the sidebar theme toggle</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if "use_demo" not in st.session_state:
    st.session_state["use_demo"] = False
if "show_dashboard" not in st.session_state:
    st.session_state["show_dashboard"] = False

if not st.session_state.get("show_dashboard", False):
    inject_styles()
    render_landing()
    render_stepper(active_step=1)

    theme_toggle(show_brand=True)

    cta1, cta2 = st.columns([3, 1])
    with cta1:
        uploaded_file = st.file_uploader(
            "Upload data source",
            type=["csv", "xlsx", "xls", "tsv", "json", "parquet"],
            help="Supported: CSV, Excel, TSV, JSON, Parquet",
        )
    with cta2:
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        if st.button("Try demo dataset", use_container_width=True):
            st.session_state["use_demo"] = True
            st.session_state["active_file"] = "__demo__"
            st.session_state["show_dashboard"] = False

    if uploaded_file is None and not st.session_state.get("use_demo", False):
        st.info("Upload a file or use the demo dataset to begin data profiling and dashboard generation.")
        st.stop()

    if uploaded_file is not None:
        st.session_state["use_demo"] = False

    current_source_name = (
        "zomato_demo_dataset.csv" if st.session_state.get("use_demo") and uploaded_file is None else uploaded_file.name
    )
    if st.session_state.get("active_file") != current_source_name:
        st.session_state["active_file"] = current_source_name
        st.session_state["show_dashboard"] = False

    with st.spinner("Reading and profiling your dataset..."):
        if st.session_state.get("use_demo") and uploaded_file is None:
            df_raw, load_error = build_demo_dataset(), None
        else:
            df_raw, load_error = load_dataset(uploaded_file)

    if load_error:
        st.error(load_error)
        st.stop()

    if df_raw is None or df_raw.empty:
        st.error("Loaded file is empty. Please upload a valid dataset.")
        st.stop()

    df_raw.columns = [str(c).strip() for c in df_raw.columns]
    cols = list(df_raw.columns)

    suggested = {
        "city": find_column(cols, ["city"]),
        "cuisine": find_column(cols, ["cuisine"]),
        "rating": find_column(cols, ["aggregate rating", "rating"]),
        "cost": find_column(cols, ["average cost for two", "cost for two", "avg cost", "cost"]),
        "votes": find_column(cols, ["votes", "vote"]),
        "latitude": find_column(cols, ["latitude", "lat"]),
        "longitude": find_column(cols, ["longitude", "lng", "lon", "long"]),
    }

    render_stepper(active_step=2)
    st.success(f"Loaded {current_source_name} with {df_raw.shape[0]:,} rows and {df_raw.shape[1]:,} columns.")

    with st.expander("Column Mapping and Data Preparation", expanded=True):
        st.write("Map your columns. Suggested fields are pre-selected.")
        options = [None] + cols

        m1, m2 = st.columns(2)
        with m1:
            city_col = st.selectbox("City column", options, index=options.index(suggested["city"]) if suggested["city"] in options else 0)
            cuisine_col = st.selectbox("Cuisine column", options, index=options.index(suggested["cuisine"]) if suggested["cuisine"] in options else 0)
            rating_col = st.selectbox("Rating column", options, index=options.index(suggested["rating"]) if suggested["rating"] in options else 0)
            cost_col = st.selectbox("Cost column", options, index=options.index(suggested["cost"]) if suggested["cost"] in options else 0)
        with m2:
            votes_col = st.selectbox("Votes column", options, index=options.index(suggested["votes"]) if suggested["votes"] in options else 0)
            lat_col = st.selectbox("Latitude column", options, index=options.index(suggested["latitude"]) if suggested["latitude"] in options else 0)
            lon_col = st.selectbox("Longitude column", options, index=options.index(suggested["longitude"]) if suggested["longitude"] in options else 0)

        mapping = {
            "city": city_col,
            "cuisine": cuisine_col,
            "rating": rating_col,
            "cost": cost_col,
            "votes": votes_col,
            "latitude": lat_col,
            "longitude": lon_col,
        }

        df = clean_with_mapping(df_raw, mapping)

        q1, q2, q3, q4 = st.columns(4)
        q1.metric("Rows", f"{len(df):,}")
        q2.metric("Columns", f"{df.shape[1]:,}")
        q3.metric("Duplicate rows", f"{int(df.duplicated().sum()):,}")
        q4.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

        if lat_col and lon_col:
            invalid_geo = int(df[[lat_col, lon_col]].isna().any(axis=1).sum())
            st.caption(f"Geo quality check: {invalid_geo:,} rows have missing or invalid latitude/longitude after cleaning.")

        st.dataframe(df.head(20), use_container_width=True, height=250)

        readiness_issues = []
        if not city_col:
            readiness_issues.append("Map a city column for geographic and city insights.")
        if not any([rating_col, cost_col, votes_col]):
            readiness_issues.append("Map at least one numeric insight column: rating, cost, or votes.")

        render_stepper(active_step=3)
        if readiness_issues:
            st.warning("Dashboard readiness checks:\n- " + "\n- ".join(readiness_issues))

        if st.button("Use this cleaned data in dashboard", type="primary", disabled=len(readiness_issues) > 0):
            st.session_state["prepared_df"] = df.copy()
            st.session_state["mapping"] = mapping
            st.session_state["source_name"] = current_source_name
            st.session_state["show_dashboard"] = True
            st.rerun()

    st.info("Review mapping and click 'Use this cleaned data in dashboard' to continue.")
    st.stop()

df = st.session_state.get("prepared_df")
mapping = st.session_state.get("mapping", {})
current_source_name = st.session_state.get("source_name", "cleaned dataset")
city_col = mapping.get("city")
cuisine_col = mapping.get("cuisine")
rating_col = mapping.get("rating")
cost_col = mapping.get("cost")
votes_col = mapping.get("votes")
lat_col = mapping.get("latitude")
lon_col = mapping.get("longitude")

if df is None or len(df) == 0:
    st.session_state["show_dashboard"] = False
    st.warning("No prepared dataset found. Please complete source mapping again.")
    st.rerun()

inject_styles()

# Dashboard header: title left, live data snapshot right
_dash_colors = get_theme_colors()
_snap_bg = "rgba(180,35,24,0.10)" if get_theme_mode() == "dark" else "rgba(180,35,24,0.06)"
_snap_border = "rgba(180,35,24,0.20)"
_snap_label = _dash_colors["sub_color"]
_snap_val = _dash_colors["heading_color"]
_snap_desc = _dash_colors["desc_color"]

_hcol1, _hcol2 = st.columns([3, 2], gap="large")
with _hcol1:
    st.markdown('<h1 class="main-title">Zomato Intelligence Dashboard</h1>', unsafe_allow_html=True)
    st.caption(f"Professional view: cleaned data from {current_source_name}")
with _hcol2:
    # Active filter summary — genuinely different from KPI cards below
    _active_cities = df[city_col].dropna().unique().tolist() if city_col else []
    _city_summary = f"All {len(_active_cities)} cities" if city_col else "—"
    _rating_summary = f"{df[rating_col].min():.1f} – {df[rating_col].max():.1f} ★" if rating_col and df[rating_col].notna().any() else "—"
    _cost_summary = f"₹{int(df[cost_col].min()):,} – ₹{int(df[cost_col].max()):,}" if cost_col and df[cost_col].notna().any() else "—"
    _top_city = df[city_col].value_counts().idxmax() if city_col else "—"
    st.markdown(
        f"""
        <div style="background:{_snap_bg};border:1px solid {_snap_border};border-radius:16px;padding:14px 18px;margin-top:6px;">
          <div style="font-size:0.72rem;font-weight:600;letter-spacing:1px;color:{_snap_label};margin-bottom:10px;">🔍 CURRENT VIEW</div>
          <div style="display:flex;flex-direction:column;gap:8px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span style="font-size:0.8rem;color:{_snap_label};">📍 Cities</span>
              <span style="font-size:0.85rem;font-weight:700;color:{_snap_val};">{_city_summary}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span style="font-size:0.8rem;color:{_snap_label};">⭐ Rating range</span>
              <span style="font-size:0.85rem;font-weight:700;color:{_snap_val};">{_rating_summary}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;">
              <span style="font-size:0.8rem;color:{_snap_label};">💰 Cost range</span>
              <span style="font-size:0.85rem;font-weight:700;color:{_snap_val};">{_cost_summary}</span>
            </div>
            <div style="border-top:1px solid {_snap_border};margin-top:2px;padding-top:8px;display:flex;justify-content:space-between;align-items:center;">
              <span style="font-size:0.8rem;color:{_snap_label};">🏆 Top city</span>
              <span style="font-size:0.85rem;font-weight:700;color:#B42318;">{_top_city}</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.header("Filters")
if st.sidebar.button("Back to Source Page"):
    st.session_state["show_dashboard"] = False
    st.rerun()

theme_toggle()

filtered = df.copy()

if city_col:
    city_options = sorted([
        c for c in filtered[city_col].dropna().unique()
        if str(c).strip() != "" and str(c).strip().lower() not in {"nan", "none"}
    ])
    selected_cities = st.sidebar.multiselect("City", city_options, default=city_options)
    if selected_cities:
        filtered = filtered[filtered[city_col].isin(selected_cities)]

if rating_col and filtered[rating_col].notna().any():
    rmin = float(filtered[rating_col].min())
    rmax = float(filtered[rating_col].max())
    rating_range = st.sidebar.slider("Rating range", rmin, rmax, (rmin, rmax))
    filtered = filtered[(filtered[rating_col] >= rating_range[0]) & (filtered[rating_col] <= rating_range[1])]

if cost_col and filtered[cost_col].notna().any():
    cmin = float(filtered[cost_col].min())
    cmax = float(filtered[cost_col].max())
    cost_range = st.sidebar.slider("Cost range", cmin, cmax, (cmin, cmax))
    filtered = filtered[(filtered[cost_col] >= cost_range[0]) & (filtered[cost_col] <= cost_range[1])]

top_n = st.sidebar.slider("Top N items for ranking charts", min_value=5, max_value=25, value=10, step=1)
show_all_sections = st.sidebar.checkbox("Show all sections on one page", value=False)

if len(filtered) == 0:
    st.warning("No data available for current filters. Please widen your filter range.")
    st.stop()

cuisine_expanded = None
if cuisine_col:
    cuisine_expanded = filtered[[cuisine_col]].dropna().copy()
    cuisine_expanded[cuisine_col] = cuisine_expanded[cuisine_col].astype(str).str.split(",")
    cuisine_expanded = cuisine_expanded.explode(cuisine_col)
    cuisine_expanded[cuisine_col] = cuisine_expanded[cuisine_col].str.strip()
    cuisine_expanded = cuisine_expanded[cuisine_expanded[cuisine_col] != ""]

city_agg = None
if city_col:
    city_agg = (
        filtered.groupby(city_col, dropna=True)
        .agg(
            restaurants=(city_col, "count"),
            avg_rating=(rating_col, "mean") if rating_col else (city_col, "count"),
            total_votes=(votes_col, "sum") if votes_col else (city_col, "count"),
            avg_cost=(cost_col, "mean") if cost_col else (city_col, "count"),
        )
        .reset_index()
    )

if city_agg is not None and rating_col and votes_col:
    city_agg["rating_norm"] = minmax(city_agg["avg_rating"])
    city_agg["votes_norm"] = minmax(city_agg["total_votes"])
    city_agg["density_norm"] = minmax(city_agg["restaurants"])
    city_agg["opportunity_score"] = (
        0.45 * city_agg["rating_norm"]
        + 0.35 * city_agg["votes_norm"]
        - 0.20 * city_agg["density_norm"]
    )

avg_rating = filtered[rating_col].mean() if rating_col and filtered[rating_col].notna().any() else np.nan
avg_cost = filtered[cost_col].mean() if cost_col and filtered[cost_col].notna().any() else np.nan
total_votes = filtered[votes_col].sum() if votes_col and filtered[votes_col].notna().any() else np.nan

if rating_col and votes_col:
    wr_df = filtered[[rating_col, votes_col]].dropna(subset=[rating_col, votes_col]).copy()
    wr_df = wr_df[wr_df[votes_col] > 0]
    weighted_rating = (wr_df[rating_col] * wr_df[votes_col]).sum() / wr_df[votes_col].sum() if len(wr_df) > 0 else np.nan
else:
    weighted_rating = np.nan

median_cost = filtered[cost_col].median() if cost_col and filtered[cost_col].notna().any() else np.nan
rated_count = filtered[rating_col].notna().sum() if rating_col else 0

if show_all_sections:
    tabs = [st.container(), st.container(), st.container(), st.container(), st.container()]
else:
    tabs = st.tabs(["Overview", "Cuisine", "Geo", "Data", "3D Space"])

with tabs[0]:
    st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Core KPIs and market-level trends</div>', unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Restaurants", f"{len(filtered):,}")
    k2.metric("Avg Rating", f"{avg_rating:.2f}" if pd.notna(avg_rating) else "NA")
    k3.metric("Weighted Rating", f"{weighted_rating:.2f}" if pd.notna(weighted_rating) else "NA")
    k4.metric("Avg Cost for Two", f"{avg_cost:,.0f}" if pd.notna(avg_cost) else "NA")
    k5.metric("Total Votes", f"{total_votes:,.0f}" if pd.notna(total_votes) else "NA")

    c1, c2 = st.columns(2)
    with c1:
        if city_agg is not None and city_col:
            top_city = city_agg.sort_values("restaurants", ascending=False).head(top_n)
            fig_city_count = px.bar(
                top_city.sort_values("restaurants"),
                x="restaurants",
                y=city_col,
                orientation="h",
                text="restaurants",
                color_discrete_sequence=[THEME_PRIMARY],
            )
            fig_city_count.update_traces(textposition="outside", cliponaxis=False, name="Restaurants", showlegend=True)
            fig_city_count = style_figure(fig_city_count, f"Top {top_n} Cities by Restaurant Count")
            st.plotly_chart(fig_city_count, use_container_width=True)
        else:
            st.info("City column not detected.")

    with c2:
        if rating_col:
            rating_band_df = filtered[[rating_col]].dropna().copy()
            rating_band_df["rating_band"] = pd.cut(
                rating_band_df[rating_col],
                bins=[0, 2, 3, 4, 5],
                labels=["0-2", "2-3", "3-4", "4-5"],
                include_lowest=True,
            )
            band_counts = (
                rating_band_df["rating_band"]
                .value_counts()
                .reindex(["0-2", "2-3", "3-4", "4-5"], fill_value=0)
                .reset_index()
            )
            band_counts.columns = ["rating_band", "count"]
            fig_band = px.bar(
                band_counts,
                x="rating_band",
                y="count",
                text="count",
                color="rating_band",
                color_discrete_sequence=[THEME_DARK, THEME_PRIMARY, "#F97066", THEME_SECONDARY],
            )
            fig_band.update_traces(textposition="outside", cliponaxis=False, showlegend=True)
            fig_band = style_figure(fig_band, "Rating Band Distribution")
            st.plotly_chart(fig_band, use_container_width=True)
        else:
            st.info("Rating column not detected.")

with tabs[1]:
    st.markdown('<div class="section-title">Cuisine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Cuisine demand, quality, and pricing insights</div>', unsafe_allow_html=True)

    if cuisine_expanded is None or cuisine_expanded.empty:
        st.warning("Cuisine column not detected or no cuisine data after filtering.")
    else:
        cuisine_counts = cuisine_expanded[cuisine_col].value_counts().head(top_n).reset_index()
        cuisine_counts.columns = ["Cuisine", "Count"]
        top_cuisine_names = cuisine_counts["Cuisine"].tolist()

        c5, c6 = st.columns(2)
        with c5:
            fig_c_count = px.bar(
                cuisine_counts.sort_values("Count"),
                x="Count",
                y="Cuisine",
                orientation="h",
                text="Count",
                color_discrete_sequence=[THEME_PRIMARY],
            )
            fig_c_count.update_traces(textposition="outside", cliponaxis=False, name="Restaurants", showlegend=True)
            fig_c_count = style_figure(fig_c_count, f"Top {top_n} Cuisines by Restaurant Count")
            st.plotly_chart(fig_c_count, use_container_width=True)

        with c6:
            if city_col and cuisine_col:
                c_city = filtered[[city_col, cuisine_col]].dropna().copy()
                c_city[cuisine_col] = c_city[cuisine_col].astype(str).str.split(",")
                c_city = c_city.explode(cuisine_col)
                c_city[cuisine_col] = c_city[cuisine_col].str.strip()
                top_cities = c_city[city_col].value_counts().head(8).index.tolist()
                c_city = c_city[c_city[cuisine_col].isin(top_cuisine_names[:8]) & c_city[city_col].isin(top_cities)]
                heat = c_city.pivot_table(index=cuisine_col, columns=city_col, aggfunc="size", fill_value=0)
                fig_heat = px.imshow(
                    heat,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale="Cividis",
                    labels={"x": "City", "y": "Cuisine", "color": "Count"},
                )
                fig_heat.update_xaxes(tickangle=-30)
                fig_heat = style_figure(fig_heat, "Cuisine Presence Across Top Cities")
                st.plotly_chart(fig_heat, use_container_width=True)
            else:
                st.info("City or cuisine column not detected.")

with tabs[2]:
    st.markdown('<div class="section-title">Geo</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Spatial patterns and city-level opportunity</div>', unsafe_allow_html=True)

    if lat_col and lon_col:
        map_df = filtered[[lat_col, lon_col]].dropna().copy()
        map_df[lat_col] = to_numeric_series(map_df[lat_col])
        map_df[lon_col] = to_numeric_series(map_df[lon_col])
        map_df = map_df.dropna()
        if len(map_df) > 0:
            center_lat = float(map_df[lat_col].mean())
            center_lon = float(map_df[lon_col].mean())
            fig_map = px.scatter_map(map_df, lat=lat_col, lon=lon_col, zoom=4, height=560)
            fig_map.update_traces(marker=dict(size=7, color=THEME_PRIMARY, opacity=0.65))
            colors = get_theme_colors()
            fig_map.update_layout(
                map_style="open-street-map",
                map=dict(
                    center=dict(lat=center_lat, lon=center_lon),
                    domain=dict(x=[0, 1], y=[0, 1]),
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor=colors["chart_paper_bg"],
                plot_bgcolor=colors["chart_plot_bg"],
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("Latitude/Longitude present but no valid numeric points after cleaning.")
    else:
        st.info("Latitude/Longitude columns not detected.")

    st.markdown('<div class="section-title">City Snapshot</div>', unsafe_allow_html=True)
    if city_agg is not None and city_col:
        show_cols = [city_col, "restaurants", "avg_rating", "total_votes", "avg_cost"]
        if "opportunity_score" in city_agg.columns:
            show_cols.append("opportunity_score")
        st.dataframe(city_agg.sort_values("restaurants", ascending=False).head(top_n)[show_cols], use_container_width=True, height=420)
    else:
        st.info("City column not detected.")

with tabs[3]:
    st.markdown('<div class="section-title">Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Filtered sample, quality checks, and export</div>', unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    d1.metric("Rows after filters", f"{len(filtered):,}")
    d2.metric("Rated restaurants", f"{rated_count:,}")
    d3.metric("Median cost for two", f"{median_cost:,.0f}" if pd.notna(median_cost) else "NA")

    st.subheader("Filtered Data Preview")
    st.dataframe(filtered.head(100), use_container_width=True, height=380)

    quality = pd.DataFrame(
        {
            "Column": filtered.columns,
            "Missing Values": [int(filtered[c].isna().sum()) for c in filtered.columns],
            "Data Type": [str(filtered[c].dtype) for c in filtered.columns],
        }
    )
    st.subheader("Data Quality Summary")
    st.dataframe(quality.sort_values("Missing Values", ascending=False), use_container_width=True, height=300)

    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data (CSV)",
        data=csv_data,
        file_name="zomato_filtered_data.csv",
        mime="text/csv",
    )

    with st.expander("Detected Columns"):
        st.write(
            {
                "city_col": city_col,
                "cuisine_col": cuisine_col,
                "rating_col": rating_col,
                "cost_col": cost_col,
                "votes_col": votes_col,
                "lat_col": lat_col,
                "lon_col": lon_col,
                "top_n": top_n,
            }
        )

with tabs[4]:
    st.markdown('<div class="section-title">3D Restaurant Space</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Rating, cost, and vote intensity in one interactive view</div>', unsafe_allow_html=True)

    if rating_col and cost_col and votes_col:
        space_df = filtered[[rating_col, cost_col, votes_col] + ([city_col] if city_col else [])].dropna().copy()
        space_df[rating_col] = to_numeric_series(space_df[rating_col])
        space_df[cost_col] = to_numeric_series(space_df[cost_col])
        space_df[votes_col] = to_numeric_series(space_df[votes_col]).clip(lower=0)
        space_df = space_df.dropna(subset=[rating_col, cost_col, votes_col])
        if len(space_df) > 0:
            fig_3d = px.scatter_3d(
                space_df.sample(min(5000, len(space_df)), random_state=42),
                x=rating_col,
                y=cost_col,
                z=votes_col,
                color=city_col if city_col else None,
                size=votes_col,
                opacity=0.72,
                color_discrete_sequence=[THEME_PRIMARY, THEME_DARK, "#F97066", THEME_SECONDARY, "#D92D20", "#F04438"],
                labels={rating_col: "Rating", cost_col: "Cost for Two", votes_col: "Votes"},
            )
            colors = get_theme_colors()
            fig_3d.update_layout(
                title="Rating × Cost × Votes",
                height=620,
                paper_bgcolor=colors["chart_paper_bg"],
                plot_bgcolor=colors["chart_plot_bg"],
                font=dict(color=colors["chart_font"]),
                margin=dict(l=0, r=0, t=45, b=0),
                legend=dict(font=dict(color=colors["chart_font"])),
                scene=dict(
                    bgcolor=colors["chart_plot_bg"],
                    xaxis=dict(title="Rating", color=colors["chart_font"], gridcolor=colors["chart_grid"]),
                    yaxis=dict(title="Cost for Two", color=colors["chart_font"], gridcolor=colors["chart_grid"]),
                    zaxis=dict(title="Votes", color=colors["chart_font"], gridcolor=colors["chart_grid"]),
                ),
            )
            st.plotly_chart(fig_3d, use_container_width=True)
        else:
            st.info("No valid rating, cost, and vote rows are available for the 3D view.")
    else:
        st.info("Map rating, cost, and votes columns to enable the 3D restaurant space.")