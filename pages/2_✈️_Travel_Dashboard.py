import pathlib
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Travel Dashboard", page_icon="✈️", layout="wide")

# ── Airline-website theme: white main content + deep navy sidebar ─────────────
T_PRIMARY  = "#0369A1"
T_ACCENT   = "#EA580C"
T_LIGHT    = "#38BDF8"
T_GREEN    = "#16A34A"
T_RED      = "#DC2626"
T_NAVY     = "#0C2D48"
T_NAVY2    = "#0F3A5C"
T_APP_BG   = "linear-gradient(160deg, #F0F9FF 0%, #FFFFFF 50%, #FFF7ED 100%)"
T_CARD     = "#FFFFFF"
T_BORDER   = "#CBD5E1"
T_TEXT     = "#0C1A2E"
T_SUB      = "#475569"
CHART_H    = 380
AIRLINE_PAL = ["#0369A1", "#EA580C", "#16A34A", "#DC2626", "#7C3AED", "#D97706"]
TIME_ORDER  = ["Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"]
TIME_LABEL  = {t: t.replace("_", " ") for t in TIME_ORDER}

COL_KEYWORDS = {
    "airline":          ["airline", "carrier", "air company", "airways"],
    "source_city":      ["source", "origin", "from", "departure city", "src city"],
    "destination_city": ["destination", "dest", "to", "arrival city", "dst city"],
    "departure_time":   ["departure time", "dep time", "depart"],
    "arrival_time":     ["arrival time", "arr time", "arrive"],
    "stops":            ["stop", "layover"],
    "class":            ["class", "seat class", "travel class", "cabin"],
    "duration":         ["duration", "flight time", "total time"],
    "days_left":        ["days left", "days before", "booking lead", "advance"],
    "price":            ["price", "fare", "cost", "ticket"],
}


def find_col(columns, keys):
    norm = {c: c.lower().replace("_", " ").strip() for c in columns}
    for col, n in norm.items():
        for k in keys:
            if k in n:
                return col
    return None


def inject_styles(is_dashboard=False):
    # Dashboard uses a light blue tint so white chart backgrounds create contrast
    app_bg = "linear-gradient(160deg, #EFF6FF 0%, #E8F4FD 45%, #EFF6FF 100%)" if is_dashboard else T_APP_BG
    st.markdown(f"""
    <style>
    .stApp {{
        background: {app_bg};
        color: {T_TEXT};
    }}
    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {T_NAVY} 0%, {T_NAVY2} 100%);
        border-right: none;
    }}
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarNav"] a {{ color: #F0F9FF !important; }}
    /* Scope all white-text overrides strictly to the sidebar */
    [data-testid="stSidebar"] button,
    [data-testid="stSidebar"] button * {{ color: #F0F9FF !important; }}
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] *,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] * {{ color: #F0F9FF !important; }}
    [data-testid="stSidebar"] [data-testid="stSlider"] label,
    [data-testid="stSidebar"] [data-testid="stSlider"] span {{ color: #F0F9FF !important; }}
    [data-testid="stSidebar"] [data-testid="stFileUploader"] * {{ color: #F0F9FF !important; }}
    [data-testid="stSidebar"] [data-testid="stExpander"] summary,
    [data-testid="stSidebar"] .streamlit-expanderHeader,
    [data-testid="stSidebar"] .streamlit-expanderHeader * {{ color: #F0F9FF !important; }}
    /* Main content: ensure all text is dark and visible */
    [data-baseweb="tab"] div, [data-baseweb="tab"] span,
    [role="tab"], [role="tab"] * {{ color: {T_TEXT} !important; }}
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stCaptionContainer"],
    label {{ color: {T_TEXT} !important; }}
    /* EaseMyTrip demo button — white text on its dark background */
    .block-container [data-testid="stButton"] button {{ color: #F0F9FF !important; }}
    .block-container [data-testid="stButton"] button p {{ color: #F0F9FF !important; }}
    /* Sidebar Back button — must stay white on dark navy */
    [data-testid="stSidebar"] [data-testid="stButton"] button p,
    [data-testid="stSidebar"] [data-testid="stButton"] button {{ color: #F0F9FF !important; }}
    [data-testid="stExpander"] summary,
    .streamlit-expanderHeader,
    .streamlit-expanderHeader * {{ color: {T_TEXT} !important; }}
    .block-container {{ padding-top: 1.8rem; padding-bottom: 1.2rem; }}
    .main-title {{
        font-size: 2.2rem; font-weight: 800; color: {T_TEXT};
        line-height: 1.2; margin-bottom: 0.1rem;
    }}
    .dash-sub {{ color: {T_SUB}; font-size: 0.95rem; margin-bottom: 0.8rem; }}
    .hero-card {{
        background: {T_CARD}; border: 1px solid {T_BORDER};
        border-radius: 18px; padding: 22px 24px;
        box-shadow: 0 2px 12px rgba(3,105,161,0.08); margin-bottom: 1rem;
    }}
    .feature-grid {{
        display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 12px; margin-top: 10px;
    }}
    .feat-item {{
        background: #F0F9FF; border: 1px solid {T_BORDER};
        border-radius: 12px; padding: 10px 12px; color: {T_TEXT};
    }}
    .stepper {{
        display: grid; grid-template-columns: repeat(4,minmax(0,1fr)); gap: 8px; margin: 12px 0 4px 0;
    }}
    .step {{
        padding: 8px 10px; border-radius: 999px; font-size: 0.82rem; text-align: center;
        border: 1px solid {T_BORDER}; color: {T_SUB}; background: #FFFFFF;
    }}
    .step.active {{
        border-color: {T_PRIMARY}; color: #FFFFFF; background: {T_PRIMARY}; font-weight: 700;
    }}
    .kpi-card {{
        background: {T_CARD}; border: 1px solid {T_BORDER}; border-radius: 14px;
        padding: 12px 10px; text-align: center;
        box-shadow: 0 1px 4px rgba(3,105,161,0.07);
    }}
    .kpi-val  {{ font-size: 1.4rem; font-weight: 800; color: {T_PRIMARY}; }}
    .kpi-lbl  {{ font-size: 0.68rem; color: {T_SUB}; margin-top: 2px; letter-spacing: 0.5px; text-transform: uppercase; }}
    .kpi-icon {{ font-size: 1.2rem; }}
    .sec-title {{
        font-size: 1rem; font-weight: 700; color: {T_TEXT};
        margin: 0.4rem 0 0.4rem 0; border-left: 3px solid {T_PRIMARY}; padding-left: 8px;
    }}
    [data-testid="stMetric"] {{
        background: {T_CARD}; border: 1px solid {T_BORDER}; border-radius: 12px; padding: 10px 12px;
    }}
    [data-testid="stMetricLabel"] p {{ color: {T_SUB} !important; }}
    [data-testid="stMetricValue"] div {{ color: {T_PRIMARY} !important; font-weight: 800 !important; }}
    [data-testid="stDataFrame"] {{
        border: 1px solid {T_BORDER}; border-radius: 10px; overflow: hidden;
    }}
    </style>
    """, unsafe_allow_html=True)


def render_stepper(active):
    labels = ["1. Source", "2. Mapping", "3. Quality", "4. Dashboard"]
    html = '<div class="stepper">'
    for i, lbl in enumerate(labels, 1):
        cls = "step active" if i == active else "step"
        html += f'<div class="{cls}">{lbl}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def style_fig(fig, title="", height=CHART_H):
    """Light airline-website chart theme — white bg, clean gridlines."""
    fig.update_layout(
        title=title,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#F8FAFC",
        font=dict(color=T_TEXT, size=12),
        title_font=dict(size=14, color=T_TEXT),
        margin=dict(l=10, r=10, t=40 if title else 12, b=12),
        height=height,
        legend=dict(font=dict(color=T_TEXT), bgcolor="rgba(0,0,0,0)", bordercolor=T_BORDER),
        coloraxis_colorbar=dict(tickfont=dict(color=T_TEXT), title_font=dict(color=T_TEXT)),
    )
    fig.update_xaxes(
        gridcolor="#E2E8F0", tickfont=dict(color=T_SUB),
        title_font=dict(color=T_TEXT), linecolor="#CBD5E1", zeroline=False,
    )
    fig.update_yaxes(
        gridcolor="#E2E8F0", tickfont=dict(color=T_SUB),
        title_font=dict(color=T_TEXT), linecolor="#CBD5E1", zeroline=False,
    )
    return fig


def to_numeric(s):
    return pd.to_numeric(s.astype(str).str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")


def load_file(uploaded):
    import pathlib as _pl
    ext = _pl.Path(uploaded.name).suffix.lower()
    try:
        if ext in {".xlsx", ".xls"}:
            uploaded.seek(0); return pd.read_excel(uploaded), None
        if ext == ".tsv":
            uploaded.seek(0); return pd.read_csv(uploaded, sep="\t"), None
        if ext == ".json":
            uploaded.seek(0); return pd.read_json(uploaded), None
        if ext == ".parquet":
            uploaded.seek(0); return pd.read_parquet(uploaded), None
        for enc in ["utf-8", "utf-8-sig", "latin-1"]:
            try:
                uploaded.seek(0)
                return pd.read_csv(uploaded, sep=None, engine="python", encoding=enc), None
            except Exception:
                continue
        return None, "Could not parse CSV with supported encodings."
    except Exception as ex:
        return None, str(ex)


def clean_df(raw, mapping):
    df = raw.copy()
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    for key in ["price", "duration", "days_left"]:
        mc = mapping.get(key)
        if mc and mc in df.columns:
            df[mc] = to_numeric(df[mc])
    return df


def build_demo():
    p = pathlib.Path(__file__).parent.parent / "data" / "travel" / "Clean_Dataset.csv"
    if p.exists():
        return pd.read_csv(p, index_col=0), None
    return None, f"Demo file not found at {p}"


# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("t_show_dash", False), ("t_df", None), ("t_map", {}),
              ("t_src", None), ("t_use_demo", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

inject_styles(is_dashboard=st.session_state.get("t_show_dash", False))

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE / ONBOARDING PAGE
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state["t_show_dash"]:

    st.sidebar.markdown(f"""
    <div style="background:linear-gradient(135deg,#0369A1,#075985);border-radius:14px;
                padding:16px 12px 12px;margin-bottom:14px;text-align:center;
                border:1px solid rgba(255,255,255,0.12);">
      <div style="font-size:2.2rem;">✈️</div>
      <div style="font-size:1.15rem;font-weight:800;color:#FFFFFF;letter-spacing:1.5px;">TRAVEL INTEL</div>
      <div style="font-size:0.68rem;color:rgba(255,255,255,0.65);margin-top:3px;">Flight Price Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">✈️ Travel Price Intelligence</h1>', unsafe_allow_html=True)
    st.caption("Upload any flight pricing dataset, map columns, and explore interactive fare analytics.")

    st.markdown(f"""
    <div class="hero-card">
      <h3 style="margin:0 0 6px 0;color:{T_TEXT};">Flight Fare Analytics Platform</h3>
      <p style="margin:0 0 10px 0;color:{T_SUB};">
        Auto-detect airlines, routes, and pricing signals from any structured flight dataset.
      </p>
      <div class="feature-grid">
        <div class="feat-item"><strong>📂 Flexible Upload</strong><br>
          <span style="color:{T_SUB};font-size:0.82rem;">CSV, Excel, TSV, JSON, Parquet</span></div>
        <div class="feat-item"><strong>🗺️ Route Heatmaps</strong><br>
          <span style="color:{T_SUB};font-size:0.82rem;">Source × Destination fare matrix</span></div>
        <div class="feat-item"><strong>⏰ Timing Analysis</strong><br>
          <span style="color:{T_SUB};font-size:0.82rem;">Best time to fly + booking lead trends</span></div>
        <div class="feat-item"><strong>📦 Box & Violin Plots</strong><br>
          <span style="color:{T_SUB};font-size:0.82rem;">Airline price distribution deep dive</span></div>
        <div class="feat-item"><strong>💰 Fare Optimizer</strong><br>
          <span style="color:{T_SUB};font-size:0.82rem;">Price vs days-left trend + median line</span></div>
        <div class="feat-item"><strong>🔬 14 Chart Types</strong><br>
          <span style="color:{T_SUB};font-size:0.82rem;">Bar, donut, scatter, heatmap, violin...</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    render_stepper(1)

    up1, up2 = st.columns([3, 1])
    with up1:
        uploaded = st.file_uploader("Upload flight dataset",
                                    type=["csv", "xlsx", "xls", "tsv", "json", "parquet"],
                                    help="Supported: CSV, Excel, TSV, JSON, Parquet")
    with up2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Use EaseMyTrip demo", use_container_width=True):
            st.session_state["t_use_demo"] = True

    if uploaded is None and not st.session_state["t_use_demo"]:
        st.info("Upload a flight dataset or click 'Use EaseMyTrip demo' to begin.")
        st.stop()

    if uploaded is not None:
        st.session_state["t_use_demo"] = False

    with st.spinner("Loading dataset..."):
        if st.session_state["t_use_demo"] and uploaded is None:
            raw_df, err = build_demo()
            src_name = "easemytrip_demo.csv"
        else:
            raw_df, err = load_file(uploaded)
            src_name = uploaded.name

    if err:
        st.error(err); st.stop()
    if raw_df is None or raw_df.empty:
        st.error("File is empty."); st.stop()

    raw_df = raw_df.loc[:, ~raw_df.columns.str.match(r"^Unnamed")]
    raw_df.columns = [c.strip() for c in raw_df.columns]
    cols = list(raw_df.columns)
    suggested = {k: find_col(cols, v) for k, v in COL_KEYWORDS.items()}

    render_stepper(2)
    st.success(f"Loaded **{src_name}** — {raw_df.shape[0]:,} rows · {raw_df.shape[1]} columns")

    with st.expander("Column Mapping", expanded=True):
        st.write("Map your flight dataset columns. Suggested fields are pre-filled.")
        opts = [None] + cols
        m1, m2 = st.columns(2)

        def sel(label, key, col):
            idx = opts.index(suggested[key]) if suggested[key] in opts else 0
            return col.selectbox(label, opts, index=idx)

        with m1:
            c_airline  = sel("Airline",          "airline",          m1)
            c_src      = sel("Source City",       "source_city",      m1)
            c_dst      = sel("Destination City",  "destination_city", m1)
            c_dep      = sel("Departure Time",    "departure_time",   m1)
            c_arr      = sel("Arrival Time",      "arrival_time",     m1)
        with m2:
            c_stops    = sel("Stops",             "stops",            m2)
            c_class    = sel("Class",             "class",            m2)
            c_duration = sel("Duration",          "duration",         m2)
            c_days     = sel("Days Left",         "days_left",        m2)
            c_price    = sel("Price",             "price",            m2)

        mapping = {
            "airline": c_airline, "source_city": c_src, "destination_city": c_dst,
            "departure_time": c_dep, "arrival_time": c_arr, "stops": c_stops,
            "class": c_class, "duration": c_duration, "days_left": c_days, "price": c_price,
        }

        df_clean = clean_df(raw_df, mapping)

        q1, q2, q3, q4 = st.columns(4)
        q1.metric("Rows",       f"{len(df_clean):,}")
        q2.metric("Columns",    f"{df_clean.shape[1]}")
        q3.metric("Duplicates", f"{int(df_clean.duplicated().sum()):,}")
        q4.metric("Missing",    f"{int(df_clean.isna().sum().sum()):,}")

        st.dataframe(df_clean.head(20), use_container_width=True, height=240)

        render_stepper(3)

        issues = []
        if not c_airline: issues.append("Map an Airline column.")
        if not c_price:   issues.append("Map a Price column.")
        if not (c_src and c_dst): issues.append("Map Source City and Destination City.")

        if issues:
            st.warning("Readiness issues:\n- " + "\n- ".join(issues))

        if st.button("Launch Dashboard →", type="primary", disabled=len(issues) > 0):
            st.session_state["t_df"]       = df_clean.copy()
            st.session_state["t_map"]      = mapping
            st.session_state["t_src"]      = src_name
            st.session_state["t_show_dash"] = True
            st.rerun()

    st.info("Review column mapping then click 'Launch Dashboard →' to continue.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ══════════════════════════════════════════════════════════════════════════════
raw      = st.session_state["t_df"]
mp       = st.session_state["t_map"]
src_name = st.session_state.get("t_src", "dataset")

if raw is None:
    st.warning("No dataset found. Please go back.")
    if st.button("← Back to Source"):
        st.session_state["t_show_dash"] = False
        st.rerun()
    st.stop()

# Rename mapped columns to standard names
rename = {v: k for k, v in mp.items() if v}
df_dash = raw.rename(columns=rename).copy()

# Normalise stops to human-readable labels
if "stops" in df_dash.columns:
    def norm_stop(x):
        s = str(x).lower().strip()
        if s in ("zero", "0", "non-stop", "nonstop", "no stop"): return "Non-stop"
        if s in ("one", "1"):                                      return "1 Stop"
        return "2+ Stops"
    df_dash["stops_label"] = df_dash["stops"].map(norm_stop)
else:
    df_dash["stops_label"] = "Unknown"

# Normalise time labels
for tc, lc in [("departure_time", "dep_label"), ("arrival_time", "arr_label")]:
    if tc in df_dash.columns:
        df_dash[lc] = df_dash[tc].astype(str).str.replace("_", " ").str.strip()
    else:
        df_dash[lc] = "Unknown"

if "airline" in df_dash.columns:
    df_dash["airline"] = df_dash["airline"].astype(str).str.replace("_", " ").str.strip()

if "source_city" in df_dash.columns and "destination_city" in df_dash.columns:
    df_dash["route"] = df_dash["source_city"].astype(str) + " → " + df_dash["destination_city"].astype(str)
else:
    df_dash["route"] = "Unknown Route"

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown(f"""
<div style="background:linear-gradient(135deg,#0369A1,#075985);border-radius:14px;
            padding:16px 12px 12px;margin-bottom:14px;text-align:center;
            border:1px solid rgba(255,255,255,0.12);">
  <div style="font-size:2.2rem;">✈️</div>
  <div style="font-size:1.15rem;font-weight:800;color:#FFFFFF;letter-spacing:1.5px;">TRAVEL INTEL</div>
  <div style="font-size:0.68rem;color:rgba(255,255,255,0.65);margin-top:3px;">Flight Price Analytics</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🔍 Filters")
if st.sidebar.button("← Back to Source Page"):
    st.session_state["t_show_dash"] = False
    st.rerun()

df = df_dash.copy()
has = lambda col: col in df.columns and df[col].notna().any()

if has("airline"):
    airlines = sorted(df["airline"].dropna().unique())
    sel_a = st.sidebar.multiselect("✈️ Airline", airlines, default=airlines)
    if sel_a: df = df[df["airline"].isin(sel_a)]

if has("class"):
    classes = sorted(df["class"].dropna().unique())
    sel_c = st.sidebar.multiselect("💺 Class", classes, default=classes)
    if sel_c: df = df[df["class"].isin(sel_c)]

if has("source_city"):
    srcs = sorted(df["source_city"].dropna().unique())
    sel_s = st.sidebar.multiselect("🛫 Source City", srcs, default=srcs)
    if sel_s: df = df[df["source_city"].isin(sel_s)]

if has("destination_city"):
    dsts = sorted(df["destination_city"].dropna().unique())
    sel_d = st.sidebar.multiselect("🛬 Destination City", dsts, default=dsts)
    if sel_d: df = df[df["destination_city"].isin(sel_d)]

stop_opts = sorted(df["stops_label"].dropna().unique())
if stop_opts:
    sel_st = st.sidebar.multiselect("🔁 Stops", stop_opts, default=stop_opts)
    if sel_st: df = df[df["stops_label"].isin(sel_st)]

if has("price"):
    p_min, p_max = int(df["price"].min()), int(df["price"].max())
    if p_min < p_max:
        pr = st.sidebar.slider("💰 Price Range", p_min, p_max, (p_min, p_max), step=500)
        df = df[(df["price"] >= pr[0]) & (df["price"] <= pr[1])]

if has("days_left"):
    d_min, d_max = int(df["days_left"].min()), int(df["days_left"].max())
    if d_min < d_max:
        dr = st.sidebar.slider("📅 Days Before Departure", d_min, d_max, (d_min, d_max))
        df = df[(df["days_left"] >= dr[0]) & (df["days_left"] <= dr[1])]

if df.empty:
    st.warning("No data matches current filters.")
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
h1, h2 = st.columns([3, 2], gap="large")
with h1:
    st.markdown('<h1 class="main-title">✈️ Travel Price Intelligence</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="dash-sub">Flight fare analytics · source: <b>{src_name}</b> · <b>{len(df):,}</b> flights in view</div>',
        unsafe_allow_html=True,
    )
with h2:
    cheapest = df.groupby("airline")["price"].mean().idxmin() if has("airline") and has("price") else "—"
    busiest  = df["route"].value_counts().idxmax() if "route" in df.columns else "—"
    n_src    = df["source_city"].nunique() if has("source_city") else "—"
    n_dst    = df["destination_city"].nunique() if has("destination_city") else "—"
    st.markdown(f"""
    <div style="background:{T_CARD};border:1px solid {T_BORDER};border-radius:14px;
                padding:12px 16px;margin-top:4px;box-shadow:0 2px 8px rgba(3,105,161,0.07);">
      <div style="font-size:0.65rem;font-weight:700;color:{T_SUB};letter-spacing:1px;margin-bottom:8px;">📡 LIVE SNAPSHOT</div>
      <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
        <span style="font-size:0.78rem;color:{T_SUB};">💸 Cheapest Airline (avg)</span>
        <span style="font-size:0.82rem;font-weight:700;color:{T_PRIMARY};">{cheapest}</span>
      </div>
      <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
        <span style="font-size:0.78rem;color:{T_SUB};">🔥 Busiest Route</span>
        <span style="font-size:0.82rem;font-weight:700;color:{T_ACCENT};">{busiest}</span>
      </div>
      <div style="display:flex;justify-content:space-between;">
        <span style="font-size:0.78rem;color:{T_SUB};">🏙️ Cities</span>
        <span style="font-size:0.82rem;font-weight:700;color:{T_PRIMARY};">{n_src} src · {n_dst} dst</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── KPI Strip ──────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
k1, k2, k3, k4, k5, k6 = st.columns(6)
avg_p  = df["price"].mean()     if has("price")     else np.nan
med_p  = df["price"].median()   if has("price")     else np.nan
min_p  = df["price"].min()      if has("price")     else np.nan
max_p  = df["price"].max()      if has("price")     else np.nan
avg_d  = df["duration"].mean()  if has("duration")  else np.nan
avg_dl = df["days_left"].mean() if has("days_left") else np.nan

for col, icon, val, lbl in [
    (k1, "💰", f"₹{avg_p:,.0f}"  if pd.notna(avg_p)  else "—", "Avg Fare"),
    (k2, "📊", f"₹{med_p:,.0f}"  if pd.notna(med_p)  else "—", "Median Fare"),
    (k3, "⬇️", f"₹{min_p:,.0f}"  if pd.notna(min_p)  else "—", "Cheapest"),
    (k4, "⬆️", f"₹{max_p:,.0f}"  if pd.notna(max_p)  else "—", "Priciest"),
    (k5, "⏱️", f"{avg_d:.1f}h"   if pd.notna(avg_d)  else "—", "Avg Duration"),
    (k6, "📅", f"{avg_dl:.0f}d"   if pd.notna(avg_dl) else "—", "Avg Days Left"),
]:
    col.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-val">{val}</div>
      <div class="kpi-lbl">{lbl}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🏠 Overview", "🗺️ Routes", "⏰ Timing & Stops", "🔬 Fare Deep Dive", "🧊 3D Fare Space"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-title">Avg Fare by Airline</div>', unsafe_allow_html=True)
        if has("airline") and has("price"):
            ap = df.groupby("airline")["price"].mean().sort_values().reset_index()
            fig = px.bar(ap, x="price", y="airline", orientation="h",
                         text=ap["price"].apply(lambda x: f"₹{x:,.0f}"),
                         color="price", color_continuous_scale=["#0EA5E9", "#EA580C"])
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(style_fig(fig), use_container_width=True)
        else:
            st.info("Airline or Price column not mapped.")

    with c2:
        st.markdown('<div class="sec-title">Economy vs Business Split</div>', unsafe_allow_html=True)
        if has("class"):
            cc = df["class"].value_counts().reset_index()
            cc.columns = ["class", "count"]
            fig = px.pie(cc, values="count", names="class", hole=0.58,
                         color_discrete_sequence=[T_PRIMARY, T_ACCENT])
            fig.update_traces(textfont=dict(color="white", size=13))
            st.plotly_chart(style_fig(fig, height=CHART_H), use_container_width=True)
        else:
            st.info("Class column not mapped.")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="sec-title">Price Distribution</div>', unsafe_allow_html=True)
        if has("price"):
            fig = px.histogram(df, x="price", nbins=70,
                               color_discrete_sequence=[T_PRIMARY], labels={"price": "Price (₹)"})
            fig.update_traces(opacity=0.8)
            st.plotly_chart(style_fig(fig), use_container_width=True)

    with c4:
        st.markdown('<div class="sec-title">Economy vs Business — Avg Fare per Airline</div>', unsafe_allow_html=True)
        if has("airline") and has("class") and has("price"):
            grp = df.groupby(["airline", "class"])["price"].mean().reset_index()
            fig = px.bar(grp, x="airline", y="price", color="class", barmode="group",
                         color_discrete_sequence=[T_PRIMARY, T_ACCENT],
                         text=grp["price"].apply(lambda x: f"₹{x/1000:.0f}k"))
            fig.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(style_fig(fig), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ROUTES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    if has("source_city") and has("destination_city") and has("price"):
        st.markdown('<div class="sec-title">Avg Fare Heatmap — Source × Destination (₹)</div>', unsafe_allow_html=True)
        rh = df.groupby(["source_city", "destination_city"])["price"].mean().reset_index()
        hp = rh.pivot(index="source_city", columns="destination_city", values="price")
        fig = px.imshow(hp, text_auto=".0f", aspect="auto",
                        color_continuous_scale=["#EFF6FF", "#0369A1", "#EA580C"],
                        labels={"x": "Destination", "y": "Source", "color": "Avg ₹"})
        fig.update_xaxes(tickangle=-15)
        st.plotly_chart(style_fig(fig, height=420), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-title">Busiest Routes (Flight Count)</div>', unsafe_allow_html=True)
        tr = df["route"].value_counts().head(10).reset_index()
        tr.columns = ["route", "count"]
        fig = px.bar(tr.sort_values("count"), x="count", y="route", orientation="h",
                     text="count", color_discrete_sequence=[T_PRIMARY])
        fig.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    with c2:
        st.markdown('<div class="sec-title">Most Expensive Routes (Avg Fare)</div>', unsafe_allow_html=True)
        if has("price"):
            re = df.groupby("route")["price"].mean().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(re.sort_values("price"), x="price", y="route", orientation="h",
                         text=re.sort_values("price")["price"].apply(lambda x: f"₹{x:,.0f}"),
                         color="price", color_continuous_scale=["#0EA5E9", "#EA580C", "#DC2626"])
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(style_fig(fig), use_container_width=True)

    if has("airline"):
        st.markdown('<div class="sec-title">Flight Volume by Airline per Route (Stacked)</div>', unsafe_allow_html=True)
        rar = df.groupby(["route", "airline"]).size().reset_index(name="count")
        fig = px.bar(rar, x="route", y="count", color="airline", barmode="stack",
                     color_discrete_sequence=AIRLINE_PAL)
        fig.update_xaxes(tickangle=-30)
        st.plotly_chart(style_fig(fig, height=400), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TIMING & STOPS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-title">Avg Fare by Departure Time</div>', unsafe_allow_html=True)
        if has("price"):
            known = [TIME_LABEL[t] for t in TIME_ORDER if TIME_LABEL[t] in df["dep_label"].unique()]
            order = known if known else sorted(df["dep_label"].unique())
            dp = df.groupby("dep_label")["price"].mean().reindex(order).dropna().reset_index()
            dp.columns = ["dep_label", "price"]
            fig = px.bar(dp, x="dep_label", y="price",
                         text=dp["price"].apply(lambda x: f"₹{x:,.0f}"),
                         color="price", color_continuous_scale=["#0EA5E9", "#EA580C"],
                         labels={"dep_label": "Departure Time", "price": "Avg Price (₹)"})
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(style_fig(fig), use_container_width=True)

    with c2:
        st.markdown('<div class="sec-title">Avg Fare by Number of Stops</div>', unsafe_allow_html=True)
        if has("price"):
            stop_ord = [s for s in ["Non-stop", "1 Stop", "2+ Stops"] if s in df["stops_label"].unique()]
            sp = df.groupby("stops_label")["price"].mean().reindex(stop_ord if stop_ord else None).dropna().reset_index()
            sp.columns = ["stops_label", "price"]
            fig = px.bar(sp, x="stops_label", y="price",
                         text=sp["price"].apply(lambda x: f"₹{x:,.0f}"),
                         color="price", color_continuous_scale=["#16A34A", "#EA580C", "#DC2626"],
                         labels={"stops_label": "Stops", "price": "Avg Price (₹)"})
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(style_fig(fig), use_container_width=True)

    if has("days_left") and has("price"):
        st.markdown('<div class="sec-title">Fare Trend — Price as Departure Approaches</div>', unsafe_allow_html=True)
        dl = df.groupby("days_left")["price"].mean().reset_index().sort_values("days_left")
        fig = px.line(dl, x="days_left", y="price",
                      labels={"days_left": "Days Before Departure", "price": "Avg Price (₹)"},
                      color_discrete_sequence=[T_PRIMARY])
        fig.update_traces(line=dict(width=2.5))
        fig.add_hline(y=df["price"].median(), line_dash="dash", line_color=T_ACCENT,
                      annotation_text=f"Median ₹{df['price'].median():,.0f}",
                      annotation_font_color=T_ACCENT)
        st.plotly_chart(style_fig(fig, height=340), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="sec-title">Flight Count — Departure × Arrival Time</div>', unsafe_allow_html=True)
        if "dep_label" in df.columns and "arr_label" in df.columns:
            tm = df.groupby(["dep_label", "arr_label"]).size().reset_index(name="count")
            tp = tm.pivot(index="dep_label", columns="arr_label", values="count").fillna(0)
            fig = px.imshow(tp, text_auto=True, aspect="auto",
                            color_continuous_scale=["#EFF6FF", "#0369A1"],
                            labels={"x": "Arrival Time", "y": "Departure Time", "color": "Flights"})
            st.plotly_chart(style_fig(fig, height=360), use_container_width=True)

    with c4:
        st.markdown('<div class="sec-title">Avg Duration — Stops × Class</div>', unsafe_allow_html=True)
        if has("duration") and has("class"):
            ds = df.groupby(["stops_label", "class"])["duration"].mean().reset_index()
            fig = px.bar(ds, x="stops_label", y="duration", color="class", barmode="group",
                         color_discrete_sequence=[T_PRIMARY, T_ACCENT],
                         text=ds["duration"].apply(lambda x: f"{x:.1f}h"),
                         labels={"stops_label": "Stops", "duration": "Avg Duration (hrs)"})
            fig.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(style_fig(fig, height=360), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — FARE DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-title">Duration vs Price (by Airline)</div>', unsafe_allow_html=True)
        if has("duration") and has("price") and has("airline"):
            sample = df.sample(min(6000, len(df)), random_state=42)
            fig = px.scatter(sample, x="duration", y="price", color="airline",
                             opacity=0.5, color_discrete_sequence=AIRLINE_PAL,
                             labels={"duration": "Duration (hrs)", "price": "Price (₹)"})
            st.plotly_chart(style_fig(fig), use_container_width=True)
        else:
            st.info("Duration, Price, or Airline column not mapped.")

    with c2:
        st.markdown('<div class="sec-title">Price Distribution per Airline (Box Plot)</div>', unsafe_allow_html=True)
        if has("airline") and has("price"):
            fig = px.box(df, x="airline", y="price", color="airline",
                         color_discrete_sequence=AIRLINE_PAL, points=False,
                         labels={"price": "Price (₹)"})
            st.plotly_chart(style_fig(fig), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="sec-title">Price Spread — Violin by Class</div>', unsafe_allow_html=True)
        if has("class") and has("price"):
            fig = px.violin(df, x="class", y="price", color="class", box=True,
                            color_discrete_sequence=[T_PRIMARY, T_ACCENT],
                            labels={"price": "Price (₹)"})
            st.plotly_chart(style_fig(fig), use_container_width=True)

    with c4:
        st.markdown('<div class="sec-title">Avg Price Matrix — Stops × Class</div>', unsafe_allow_html=True)
        if has("class") and has("price"):
            sc  = df.groupby(["stops_label", "class"])["price"].mean().reset_index()
            sp2 = sc.pivot(index="stops_label", columns="class", values="price")
            fig = px.imshow(sp2, text_auto=".0f", aspect="auto",
                            color_continuous_scale=["#EFF6FF", "#0369A1", "#EA580C"],
                            labels={"color": "Avg Price (₹)"})
            st.plotly_chart(style_fig(fig, height=CHART_H), use_container_width=True)

    if has("airline") and has("price"):
        st.markdown('<div class="sec-title">Avg Fare — Airline × Stops Breakdown</div>', unsafe_allow_html=True)
        as_grp = df.groupby(["airline", "stops_label"])["price"].mean().reset_index()
        fig = px.bar(as_grp, x="airline", y="price", color="stops_label", barmode="group",
                     color_discrete_sequence=[T_GREEN, T_ACCENT, T_RED],
                     text=as_grp["price"].apply(lambda x: f"₹{x/1000:.0f}k"),
                     labels={"stops_label": "Stops", "price": "Avg Price (₹)"})
        fig.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(style_fig(fig, height=400), use_container_width=True)

    if has("airline") and has("price"):
        st.markdown('<div class="sec-title">Top 12 Airline + Route Combinations</div>', unsafe_allow_html=True)
        agg_dict = {"flights": ("price", "count"), "avg_price": ("price", "mean")}
        if has("duration"):
            agg_dict["avg_duration"] = ("duration", "mean")
        combo = (
            df.groupby(["airline", "route"]).agg(**agg_dict)
            .sort_values("flights", ascending=False).head(12).reset_index()
        )
        combo["avg_price"] = combo["avg_price"].apply(lambda x: f"₹{x:,.0f}")
        if "avg_duration" in combo.columns:
            combo["avg_duration"] = combo["avg_duration"].apply(lambda x: f"{x:.1f}h")
        st.dataframe(combo, use_container_width=True, height=320)

with tabs[4]:
    st.markdown('<div class="sec-title">3D Fare Space — Days Left × Duration × Price</div>', unsafe_allow_html=True)
    if has("days_left") and has("duration") and has("price"):
        space_df = df[["days_left", "duration", "price"] + (["airline"] if has("airline") else []) + (["class"] if has("class") else [])].dropna().copy()
        space_df["marker_size"] = space_df["price"].abs().clip(lower=1)
        if len(space_df) > 0:
            sample_3d = space_df.sample(min(9000, len(space_df)), random_state=42)
            fig = px.scatter_3d(
                sample_3d,
                x="days_left",
                y="duration",
                z="price",
                color="airline" if "airline" in sample_3d.columns else None,
                symbol="class" if "class" in sample_3d.columns else None,
                size="marker_size",
                opacity=0.65,
                color_discrete_sequence=AIRLINE_PAL,
                labels={"days_left": "Days Before Departure", "duration": "Duration (hrs)", "price": "Price (₹)"},
            )
            fig.update_layout(
                title="Booking Lead Time, Flight Duration, and Fare Relationship",
                height=650,
                scene=dict(
                    bgcolor="#FFFFFF",
                    xaxis=dict(backgroundcolor="#F8FAFC", gridcolor="#CBD5E1", color=T_TEXT),
                    yaxis=dict(backgroundcolor="#F8FAFC", gridcolor="#CBD5E1", color=T_TEXT),
                    zaxis=dict(backgroundcolor="#F8FAFC", gridcolor="#CBD5E1", color=T_TEXT),
                ),
            )
            st.plotly_chart(style_fig(fig, height=650), use_container_width=True)
        else:
            st.info("No valid rows are available for the 3D fare space.")
    else:
        st.info("Map days_left, duration, and price columns to enable the 3D fare space.")
