import pathlib
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="E-commerce Dashboard", page_icon="🛒", layout="wide")

# Midnight Purple theme for a premium marketplace feel
P_BG = "linear-gradient(145deg, #12071F 0%, #241039 48%, #160B2A 100%)"
P_CARD = "#1F1233"
P_CARD_2 = "#2B1746"
P_BORDER = "#5B3C88"
P_TEXT = "#F8F4FF"
P_SUB = "#C8B6E8"
P_PRIMARY = "#A855F7"
P_ACCENT = "#F59E0B"
P_GREEN = "#22C55E"
P_RED = "#F43F5E"
P_BLUE = "#38BDF8"
P_PINK = "#EC4899"
CHART_H = 380
CAT_ICONS = {
    "Accessories": "🎧",
    "Apparel": "👕",
    "Electronics": "💻",
    "Furniture": "🛋️",
    "Stationery": "🖊️",
}
CAT_COLORS = ["#A855F7", "#F59E0B", "#38BDF8", "#22C55E", "#EC4899"]

COL_KEYWORDS = {
    "InvoiceNo": ["invoice", "order", "transaction"],
    "StockCode": ["stock", "sku", "product code"],
    "Description": ["description", "product", "item", "name"],
    "Quantity": ["quantity", "qty", "units"],
    "InvoiceDate": ["invoice date", "order date", "date"],
    "UnitPrice": ["unit price", "price"],
    "CustomerID": ["customer", "customer id"],
    "Country": ["country"],
    "Discount": ["discount"],
    "PaymentMethod": ["payment"],
    "ShippingCost": ["shipping", "delivery cost", "freight"],
    "Category": ["category"],
    "SalesChannel": ["sales channel", "channel"],
    "ReturnStatus": ["return"],
    "ShipmentProvider": ["shipment", "provider", "courier"],
    "WarehouseLocation": ["warehouse"],
    "OrderPriority": ["priority"],
}


def find_col(columns, keys):
    normalized = {col: str(col).strip().lower().replace("_", " ") for col in columns}
    for col, norm in normalized.items():
        for key in keys:
            if key in norm:
                return col
    return None


def inject_styles():
    st.markdown(f"""
    <style>
    .stApp {{ background: {P_BG}; color: {P_TEXT}; }}
    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #10051D 0%, #1A0D2E 100%);
        border-right: 1px solid {P_BORDER};
    }}
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarNav"] a {{ color: {P_TEXT} !important; }}
    [data-testid="stSidebar"] button,
    [data-testid="stSidebar"] button * {{ color: {P_TEXT} !important; }}
    [data-testid="stMultiSelect"] *, [data-testid="stSelectbox"] * {{ color: {P_TEXT} !important; }}
    [data-testid="stSlider"] label, [data-testid="stSlider"] span {{ color: {P_TEXT} !important; }}
    .block-container {{ padding-top: 1.7rem; padding-bottom: 1.2rem; }}
    .main-title {{
        font-size: 2.25rem; font-weight: 850; color: {P_TEXT}; line-height: 1.12;
        margin-bottom: 0.1rem;
    }}
    .subtle {{ color: {P_SUB}; font-size: 0.95rem; }}
    .hero-card {{
        background: linear-gradient(135deg, rgba(168,85,247,0.22), rgba(236,72,153,0.12));
        border: 1px solid {P_BORDER}; border-radius: 18px; padding: 18px 20px;
        box-shadow: 0 8px 28px rgba(0,0,0,0.22);
    }}
    .kpi-card {{
        background: {P_CARD}; border: 1px solid {P_BORDER}; border-radius: 14px;
        padding: 12px 10px; text-align: center; min-height: 92px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.14);
    }}
    .kpi-icon {{ font-size: 1.25rem; }}
    .kpi-val {{ color: {P_ACCENT}; font-size: 1.35rem; font-weight: 850; }}
    .kpi-lbl {{ color: {P_SUB}; font-size: 0.68rem; letter-spacing: 0.5px; text-transform: uppercase; }}
    .sec-title {{
        color: {P_TEXT}; font-weight: 760; font-size: 1rem; margin: 0.45rem 0 0.45rem;
        border-left: 3px solid {P_ACCENT}; padding-left: 8px;
    }}
    .tile-wrap {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 10px; margin: 10px 0 14px; }}
    .cat-tile {{
        background: {P_CARD}; border: 1px solid {P_BORDER}; border-radius: 14px; padding: 12px;
        min-height: 88px; text-align: center;
    }}
    .cat-icon {{ font-size: 1.8rem; margin-bottom: 4px; }}
    .cat-name {{ font-weight: 750; color: {P_TEXT}; font-size: 0.88rem; }}
    .cat-meta {{ color: {P_SUB}; font-size: 0.72rem; margin-top: 3px; }}
    [data-testid="stButton"] button {{
        background: linear-gradient(135deg, #7C3AED, #C026D3) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        color: {P_TEXT} !important;
        border-radius: 10px !important;
    }}
    [data-testid="stButton"] button p {{ color: {P_TEXT} !important; }}
    [data-testid="stDataFrame"] {{ border: 1px solid {P_BORDER}; border-radius: 10px; overflow: hidden; }}
    </style>
    """, unsafe_allow_html=True)


def style_fig(fig, title="", height=CHART_H):
    fig.update_layout(
        title=title,
        plot_bgcolor="#1A0D2E",
        paper_bgcolor="#12071F",
        font=dict(color=P_TEXT, size=12),
        title_font=dict(color=P_TEXT, size=14),
        margin=dict(l=10, r=10, t=42 if title else 12, b=14),
        height=height,
        legend=dict(font=dict(color=P_TEXT), bgcolor="rgba(0,0,0,0)", bordercolor=P_BORDER),
        coloraxis_colorbar=dict(tickfont=dict(color=P_TEXT), title_font=dict(color=P_TEXT)),
        scene=dict(
            bgcolor="#12071F",
            xaxis=dict(backgroundcolor="#1A0D2E", gridcolor=P_BORDER, color=P_TEXT),
            yaxis=dict(backgroundcolor="#1A0D2E", gridcolor=P_BORDER, color=P_TEXT),
            zaxis=dict(backgroundcolor="#1A0D2E", gridcolor=P_BORDER, color=P_TEXT),
        ),
    )
    fig.update_xaxes(gridcolor=P_BORDER, tickfont=dict(color=P_SUB), title_font=dict(color=P_TEXT), zeroline=False)
    fig.update_yaxes(gridcolor=P_BORDER, tickfont=dict(color=P_SUB), title_font=dict(color=P_TEXT), zeroline=False)
    return fig


def prepare_data(df):
    df.columns = [c.strip() for c in df.columns]
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    for c in ["Quantity", "UnitPrice", "Discount", "ShippingCost"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")
    defaults = {"Quantity": 0, "UnitPrice": 0, "Discount": 0, "ShippingCost": 0}
    for c, default in defaults.items():
        if c not in df.columns:
            df[c] = default
    df["Discount"] = df["Discount"].fillna(0)
    if df["Discount"].max() > 1:
        df["DiscountRate"] = df["Discount"] / 100
    else:
        df["DiscountRate"] = df["Discount"]
    df["Revenue"] = df["Quantity"] * df["UnitPrice"] * (1 - df["DiscountRate"])
    df["GrossSales"] = df["Quantity"] * df["UnitPrice"]
    df["ProfitProxy"] = df["Revenue"] - df["ShippingCost"].fillna(0)
    df["MarkerSize"] = df["Quantity"].abs().fillna(0).clip(lower=1)
    df["RevenueSize"] = df["Revenue"].abs().fillna(0).clip(lower=1)
    if "InvoiceDate" in df.columns:
        df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
        df["Quarter"] = df["InvoiceDate"].dt.to_period("Q").astype(str)
    else:
        df["Month"] = "Unknown"
        df["Quarter"] = "Unknown"
    if "ReturnStatus" in df.columns:
        status = df["ReturnStatus"].astype(str).str.lower()
        df["ReturnedFlag"] = status.str.contains("returned") & ~status.str.contains("not")
    else:
        df["ReturnedFlag"] = False
    for c in ["InvoiceNo", "Description", "Country", "PaymentMethod", "Category", "SalesChannel", "ShipmentProvider", "WarehouseLocation", "OrderPriority"]:
        if c not in df.columns:
            df[c] = "Unknown"
    return df


@st.cache_data
def load_data():
    path = pathlib.Path(__file__).parent.parent / "data" / "E-Commerce" / "online_sales_dataset.csv"
    if not path.exists():
        return None, f"Dataset not found: {path}"
    df = pd.read_csv(path)
    df = prepare_data(df)
    return df, None


def load_uploaded_file(uploaded):
    ext = pathlib.Path(uploaded.name).suffix.lower()
    try:
        if ext in {".xlsx", ".xls"}:
            uploaded.seek(0)
            return pd.read_excel(uploaded), None
        if ext == ".tsv":
            uploaded.seek(0)
            return pd.read_csv(uploaded, sep="\t"), None
        if ext == ".json":
            uploaded.seek(0)
            return pd.read_json(uploaded), None
        if ext == ".parquet":
            uploaded.seek(0)
            return pd.read_parquet(uploaded), None
        for enc in ["utf-8", "utf-8-sig", "latin-1"]:
            try:
                uploaded.seek(0)
                return pd.read_csv(uploaded, sep=None, engine="python", encoding=enc), None
            except Exception:
                continue
        return None, "Could not read CSV with supported encodings."
    except Exception as ex:
        return None, f"Failed to parse file: {ex}"


def render_stepper(active_step):
    labels = ["1. Source", "2. Mapping", "3. Quality Check", "4. Dashboard"]
    html = '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin:12px 0 4px 0;">'
    for idx, label in enumerate(labels, start=1):
        bg = "linear-gradient(135deg, #7C3AED, #C026D3)" if idx == active_step else P_CARD
        border = "rgba(255,255,255,0.28)" if idx == active_step else P_BORDER
        html += f'<div style="padding:8px 10px;border-radius:999px;text-align:center;font-size:0.84rem;font-weight:700;color:{P_TEXT};background:{bg};border:1px solid {border};">{label}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def money(v):
    if pd.isna(v):
        return "—"
    if abs(v) >= 1_000_000:
        return f"${v/1_000_000:.2f}M"
    if abs(v) >= 1_000:
        return f"${v/1_000:.1f}K"
    return f"${v:,.0f}"


inject_styles()

for key, default in [
    ("ecom_show_dash", False),
    ("ecom_df", None),
    ("ecom_source", None),
    ("ecom_use_demo", False),
    ("selected_category", "All"),
]:
    if key not in st.session_state:
        st.session_state[key] = default

if not st.session_state["ecom_show_dash"]:
    st.sidebar.markdown(f"""
    <div style="background:linear-gradient(135deg,#7C3AED,#C026D3);border-radius:16px;padding:16px 12px;text-align:center;margin-bottom:14px;">
      <div style="font-size:2.1rem;">🛒</div>
      <div style="font-weight:850;color:white;letter-spacing:1px;font-size:1.05rem;">COMMERCE LUX</div>
      <div style="color:rgba(255,255,255,0.72);font-size:0.68rem;margin-top:3px;">Premium E-commerce Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">🛒 E-commerce Performance Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">Upload retail transaction data, map columns, inspect quality, and launch a premium analytics dashboard.</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="hero-card" style="margin-top:12px;">
      <div style="font-size:1.15rem;font-weight:800;color:{P_TEXT};margin-bottom:6px;">Midnight Purple Commerce Onboarding</div>
      <div style="color:{P_SUB};margin-bottom:10px;">Designed for sales, returns, product, payment, shipping, and 3D commerce analysis.</div>
      <div class="tile-wrap">
        <div class="cat-tile"><div class="cat-icon">📂</div><div class="cat-name">Upload</div><div class="cat-meta">CSV, Excel, TSV, JSON</div></div>
        <div class="cat-tile"><div class="cat-icon">🧭</div><div class="cat-name">Mapping</div><div class="cat-meta">Flexible schema</div></div>
        <div class="cat-tile"><div class="cat-icon">🧹</div><div class="cat-name">Cleaning</div><div class="cat-meta">Revenue metrics</div></div>
        <div class="cat-tile"><div class="cat-icon">🧊</div><div class="cat-name">3D Studio</div><div class="cat-meta">Commerce universe</div></div>
        <div class="cat-tile"><div class="cat-icon">📈</div><div class="cat-name">Insights</div><div class="cat-meta">Returns + profit</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    render_stepper(1)
    c1, c2 = st.columns([3, 1])
    with c1:
        uploaded = st.file_uploader(
            "Upload e-commerce dataset",
            type=["csv", "xlsx", "xls", "tsv", "json", "parquet"],
            help="Supported: CSV, Excel, TSV, JSON, Parquet",
        )
    with c2:
        st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
        if st.button("Use Online Sales demo", use_container_width=True):
            st.session_state["ecom_use_demo"] = True

    if uploaded is None and not st.session_state["ecom_use_demo"]:
        st.info("Upload an e-commerce dataset or use the bundled Online Sales demo.")
        st.stop()

    if uploaded is not None:
        st.session_state["ecom_use_demo"] = False

    with st.spinner("Reading dataset..."):
        if st.session_state["ecom_use_demo"] and uploaded is None:
            raw_df, err = load_data()
            source_name = "online_sales_dataset.csv"
        else:
            raw_df, err = load_uploaded_file(uploaded)
            source_name = uploaded.name

    if err:
        st.error(err)
        st.stop()
    if raw_df is None or raw_df.empty:
        st.error("Loaded file is empty.")
        st.stop()

    raw_df = raw_df.loc[:, ~raw_df.columns.astype(str).str.match(r"^Unnamed")]
    raw_df.columns = [str(c).strip() for c in raw_df.columns]
    cols = list(raw_df.columns)
    suggested = {field: find_col(cols, keys) for field, keys in COL_KEYWORDS.items()}

    render_stepper(2)
    st.success(f"Loaded **{source_name}** with {len(raw_df):,} rows and {raw_df.shape[1]} columns.")
    with st.expander("Column Mapping", expanded=True):
        st.write("Map the commerce fields. Suggestions are pre-selected where possible.")
        options = [None] + cols
        left, right = st.columns(2)

        def choose(label, field, container):
            value = suggested.get(field)
            idx = options.index(value) if value in options else 0
            return container.selectbox(label, options, index=idx)

        with left:
            m_invoice = choose("Invoice / Order ID", "InvoiceNo", left)
            m_product = choose("Product Description", "Description", left)
            m_quantity = choose("Quantity", "Quantity", left)
            m_date = choose("Invoice / Order Date", "InvoiceDate", left)
            m_unit = choose("Unit Price", "UnitPrice", left)
            m_customer = choose("Customer ID", "CustomerID", left)
            m_country = choose("Country", "Country", left)
            m_discount = choose("Discount", "Discount", left)
            m_payment = choose("Payment Method", "PaymentMethod", left)
        with right:
            m_shipping = choose("Shipping Cost", "ShippingCost", right)
            m_category = choose("Category", "Category", right)
            m_channel = choose("Sales Channel", "SalesChannel", right)
            m_return = choose("Return Status", "ReturnStatus", right)
            m_provider = choose("Shipment Provider", "ShipmentProvider", right)
            m_warehouse = choose("Warehouse Location", "WarehouseLocation", right)
            m_priority = choose("Order Priority", "OrderPriority", right)
            m_stock = choose("Stock / SKU Code", "StockCode", right)

        mapping = {
            m_invoice: "InvoiceNo", m_stock: "StockCode", m_product: "Description", m_quantity: "Quantity",
            m_date: "InvoiceDate", m_unit: "UnitPrice", m_customer: "CustomerID", m_country: "Country",
            m_discount: "Discount", m_payment: "PaymentMethod", m_shipping: "ShippingCost", m_category: "Category",
            m_channel: "SalesChannel", m_return: "ReturnStatus", m_provider: "ShipmentProvider",
            m_warehouse: "WarehouseLocation", m_priority: "OrderPriority",
        }
        mapping = {k: v for k, v in mapping.items() if k}
        prepared = prepare_data(raw_df.rename(columns=mapping).copy())

        q1, q2, q3, q4 = st.columns(4)
        q1.metric("Rows", f"{len(prepared):,}")
        q2.metric("Columns", f"{prepared.shape[1]:,}")
        q3.metric("Duplicate rows", f"{int(prepared.duplicated().sum()):,}")
        q4.metric("Missing cells", f"{int(prepared.isna().sum().sum()):,}")
        st.dataframe(prepared.head(20), use_container_width=True, height=240)

        render_stepper(3)
        issues = []
        if not m_invoice:
            issues.append("Map an Invoice / Order ID column.")
        if not m_product:
            issues.append("Map a Product Description column.")
        if not m_quantity or not m_unit:
            issues.append("Map Quantity and Unit Price columns to calculate revenue.")
        if not m_category:
            issues.append("Map a Category column for tile filters.")
        if issues:
            st.warning("Readiness issues:\n- " + "\n- ".join(issues))

        if st.button("Launch E-commerce Dashboard", type="primary", disabled=len(issues) > 0):
            st.session_state["ecom_df"] = prepared.copy()
            st.session_state["ecom_source"] = source_name
            st.session_state["ecom_show_dash"] = True
            st.session_state["selected_category"] = "All"
            st.rerun()

    st.info("Review mapping and launch the dashboard when quality checks look right.")
    st.stop()

df_raw = st.session_state.get("ecom_df")
if df_raw is None or df_raw.empty:
    st.session_state["ecom_show_dash"] = False
    st.warning("No prepared e-commerce dataset found. Please complete source mapping again.")
    st.rerun()

# Sidebar brand + filters
st.sidebar.markdown(f"""
<div style="background:linear-gradient(135deg,#7C3AED,#C026D3);border-radius:16px;padding:16px 12px;text-align:center;margin-bottom:14px;">
  <div style="font-size:2.1rem;">🛒</div>
  <div style="font-weight:850;color:white;letter-spacing:1px;font-size:1.05rem;">COMMERCE LUX</div>
  <div style="color:rgba(255,255,255,0.72);font-size:0.68rem;margin-top:3px;">Premium E-commerce Intelligence</div>
</div>
""", unsafe_allow_html=True)

if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "All"

st.sidebar.markdown("### 🧭 Filters")
if st.sidebar.button("← Back to Source Page", use_container_width=True):
    st.session_state["ecom_show_dash"] = False
    st.rerun()

if st.sidebar.button("Show All Categories", use_container_width=True):
    st.session_state["selected_category"] = "All"

countries = sorted(df_raw["Country"].dropna().unique())
sel_country = st.sidebar.multiselect("🌍 Country", countries, default=countries)
channels = sorted(df_raw["SalesChannel"].dropna().unique())
sel_channel = st.sidebar.multiselect("🛍️ Sales Channel", channels, default=channels)
payments = sorted(df_raw["PaymentMethod"].dropna().unique())
sel_payment = st.sidebar.multiselect("💳 Payment Method", payments, default=payments)
priorities = sorted(df_raw["OrderPriority"].dropna().unique())
sel_priority = st.sidebar.multiselect("⚡ Order Priority", priorities, default=priorities)

rev_min, rev_max = float(df_raw["Revenue"].min()), float(df_raw["Revenue"].max())
rev_range = st.sidebar.slider("💰 Revenue per Line", float(rev_min), float(rev_max), (float(rev_min), float(rev_max)))

# Apply filters
filtered = df_raw.copy()
if st.session_state["selected_category"] != "All":
    filtered = filtered[filtered["Category"] == st.session_state["selected_category"]]
filtered = filtered[filtered["Country"].isin(sel_country)]
filtered = filtered[filtered["SalesChannel"].isin(sel_channel)]
filtered = filtered[filtered["PaymentMethod"].isin(sel_payment)]
filtered = filtered[filtered["OrderPriority"].isin(sel_priority)]
filtered = filtered[(filtered["Revenue"] >= rev_range[0]) & (filtered["Revenue"] <= rev_range[1])]

if filtered.empty:
    st.warning("No data matches current filters.")
    st.stop()

# Header
h1, h2 = st.columns([3, 2], gap="large")
with h1:
    st.markdown('<div class="main-title">🛒 E-commerce Performance Studio</div>', unsafe_allow_html=True)
    active_cat = st.session_state["selected_category"]
    st.markdown(f'<div class="subtle">Midnight Purple marketplace analytics · Active category: <b>{active_cat}</b> · {len(filtered):,} transaction lines</div>', unsafe_allow_html=True)
with h2:
    best_cat = filtered.groupby("Category")["Revenue"].sum().idxmax()
    top_country = filtered.groupby("Country")["Revenue"].sum().idxmax()
    return_rate = filtered["ReturnedFlag"].mean() * 100
    st.markdown(f"""
    <div class="hero-card">
      <div style="font-size:0.68rem;color:{P_SUB};font-weight:800;letter-spacing:1px;margin-bottom:8px;">LIVE COMMERCE SNAPSHOT</div>
      <div style="display:flex;justify-content:space-between;"><span style="color:{P_SUB};">🏆 Top Category</span><b style="color:{P_ACCENT};">{best_cat}</b></div>
      <div style="display:flex;justify-content:space-between;"><span style="color:{P_SUB};">🌍 Top Country</span><b style="color:{P_PRIMARY};">{top_country}</b></div>
      <div style="display:flex;justify-content:space-between;"><span style="color:{P_SUB};">↩️ Return Rate</span><b style="color:{P_RED};">{return_rate:.1f}%</b></div>
    </div>
    """, unsafe_allow_html=True)

# Clickable category tiles
st.markdown('<div class="sec-title">Click a Category Tile to Filter the Dashboard</div>', unsafe_allow_html=True)
cat_agg = df_raw.groupby("Category").agg(revenue=("Revenue", "sum"), orders=("InvoiceNo", "nunique")).reset_index()
cols = st.columns(len(cat_agg))
for col, (_, row) in zip(cols, cat_agg.iterrows()):
    cat = row["Category"]
    with col:
        st.markdown(f"""
        <div class="cat-tile">
          <div class="cat-icon">{CAT_ICONS.get(cat, '🛒')}</div>
          <div class="cat-name">{cat}</div>
          <div class="cat-meta">{money(row['revenue'])} · {int(row['orders']):,} orders</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Filter {cat}", key=f"cat_{cat}", use_container_width=True):
            st.session_state["selected_category"] = cat
            st.rerun()

# KPI strip
k1, k2, k3, k4, k5, k6 = st.columns(6)
kpis = [
    (k1, "💰", money(filtered["Revenue"].sum()), "Revenue"),
    (k2, "📦", f"{filtered['InvoiceNo'].nunique():,}", "Orders"),
    (k3, "🧾", money(filtered.groupby('InvoiceNo')['Revenue'].sum().mean()), "Avg Order"),
    (k4, "📈", money(filtered["ProfitProxy"].sum()), "Profit Proxy"),
    (k5, "🏷️", f"{filtered['DiscountRate'].mean()*100:.1f}%", "Avg Discount"),
    (k6, "↩️", f"{filtered['ReturnedFlag'].mean()*100:.1f}%", "Return Rate"),
]
for col, icon, val, lbl in kpis:
    col.markdown(f"""
    <div class="kpi-card"><div class="kpi-icon">{icon}</div><div class="kpi-val">{val}</div><div class="kpi-lbl">{lbl}</div></div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

tabs = st.tabs(["🏠 Executive", "🛍️ Products", "🌍 Operations", "🧊 3D Studio"])

with tabs[0]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-title">Monthly Revenue Trend</div>', unsafe_allow_html=True)
        trend = filtered.groupby("Month")["Revenue"].sum().reset_index().sort_values("Month")
        fig = px.area(trend, x="Month", y="Revenue", color_discrete_sequence=[P_PRIMARY])
        fig.update_traces(line=dict(width=2.5), fillcolor="rgba(168,85,247,0.25)")
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with c2:
        st.markdown('<div class="sec-title">Revenue by Category</div>', unsafe_allow_html=True)
        cat_rev = filtered.groupby("Category")["Revenue"].sum().sort_values().reset_index()
        fig = px.bar(cat_rev, x="Revenue", y="Category", orientation="h", color="Revenue",
                     color_continuous_scale=["#3B0764", "#A855F7", "#F59E0B"],
                     text=cat_rev["Revenue"].apply(money))
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="sec-title">Payment Method Split</div>', unsafe_allow_html=True)
        pay = filtered.groupby("PaymentMethod")["Revenue"].sum().reset_index()
        fig = px.pie(pay, names="PaymentMethod", values="Revenue", hole=0.55, color_discrete_sequence=CAT_COLORS)
        fig.update_traces(textfont=dict(color="white"))
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with c4:
        st.markdown('<div class="sec-title">Sales Channel Mix</div>', unsafe_allow_html=True)
        ch = filtered.groupby("SalesChannel")["Revenue"].sum().reset_index()
        fig = px.pie(ch, names="SalesChannel", values="Revenue", hole=0.45, color_discrete_sequence=[P_ACCENT, P_PRIMARY])
        fig.update_traces(textfont=dict(color="white"))
        st.plotly_chart(style_fig(fig), use_container_width=True)

with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-title">Top 12 Products by Revenue</div>', unsafe_allow_html=True)
        prod = filtered.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(12).reset_index()
        fig = px.bar(prod.sort_values("Revenue"), x="Revenue", y="Description", orientation="h",
                     color="Revenue", color_continuous_scale=["#3B0764", "#A855F7", "#F59E0B"],
                     text=prod.sort_values("Revenue")["Revenue"].apply(money))
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with c2:
        st.markdown('<div class="sec-title">Discount vs Revenue</div>', unsafe_allow_html=True)
        sample = filtered.sample(min(6000, len(filtered)), random_state=42)
        fig = px.scatter(sample, x="DiscountRate", y="Revenue", color="Category", size="MarkerSize",
                         color_discrete_sequence=CAT_COLORS, opacity=0.62,
                         labels={"DiscountRate": "Discount", "Revenue": "Revenue"})
        st.plotly_chart(style_fig(fig), use_container_width=True)

    st.markdown('<div class="sec-title">Category Performance Table</div>', unsafe_allow_html=True)
    table = filtered.groupby("Category").agg(
        orders=("InvoiceNo", "nunique"), quantity=("Quantity", "sum"), revenue=("Revenue", "sum"),
        avg_unit_price=("UnitPrice", "mean"), avg_discount=("DiscountRate", "mean"), return_rate=("ReturnedFlag", "mean")
    ).reset_index()
    table["revenue"] = table["revenue"].apply(money)
    table["avg_unit_price"] = table["avg_unit_price"].apply(money)
    table["avg_discount"] = table["avg_discount"].apply(lambda x: f"{x*100:.1f}%")
    table["return_rate"] = table["return_rate"].apply(lambda x: f"{x*100:.1f}%")
    st.dataframe(table, use_container_width=True, height=260)

with tabs[2]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-title">Revenue by Country</div>', unsafe_allow_html=True)
        country = filtered.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(15).reset_index()
        fig = px.bar(country, x="Country", y="Revenue", color="Revenue",
                     color_continuous_scale=["#3B0764", "#A855F7", "#F59E0B"],
                     text=country["Revenue"].apply(money))
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_coloraxes(showscale=False)
        fig.update_xaxes(tickangle=-30)
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with c2:
        st.markdown('<div class="sec-title">Return Rate by Category</div>', unsafe_allow_html=True)
        ret = filtered.groupby("Category")["ReturnedFlag"].mean().reset_index()
        ret["ReturnRatePct"] = ret["ReturnedFlag"] * 100
        fig = px.bar(ret, x="Category", y="ReturnRatePct", color="ReturnRatePct",
                     color_continuous_scale=[P_GREEN, P_ACCENT, P_RED], text=ret["ReturnRatePct"].apply(lambda x: f"{x:.1f}%"))
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="sec-title">Shipment Provider Revenue</div>', unsafe_allow_html=True)
        ship = filtered.groupby("ShipmentProvider")["Revenue"].sum().reset_index()
        fig = px.bar(ship, x="ShipmentProvider", y="Revenue", color="ShipmentProvider", color_discrete_sequence=CAT_COLORS,
                     text=ship["Revenue"].apply(money))
        fig.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(style_fig(fig), use_container_width=True)
    with c4:
        st.markdown('<div class="sec-title">Order Priority Mix</div>', unsafe_allow_html=True)
        pri = filtered.groupby("OrderPriority")["InvoiceNo"].nunique().reset_index()
        fig = px.pie(pri, names="OrderPriority", values="InvoiceNo", hole=0.5, color_discrete_sequence=[P_GREEN, P_ACCENT, P_RED])
        fig.update_traces(textfont=dict(color="white"))
        st.plotly_chart(style_fig(fig), use_container_width=True)

with tabs[3]:
    st.markdown('<div class="sec-title">3D Commerce Universe: Quantity × Unit Price × Shipping Cost</div>', unsafe_allow_html=True)
    sample3d = filtered.sample(min(9000, len(filtered)), random_state=7)
    fig = px.scatter_3d(
        sample3d, x="Quantity", y="UnitPrice", z="ShippingCost", color="Category", size="RevenueSize",
        hover_name="Description", color_discrete_sequence=CAT_COLORS, opacity=0.74,
        labels={"Quantity": "Quantity", "UnitPrice": "Unit Price", "ShippingCost": "Shipping Cost"},
    )
    st.plotly_chart(style_fig(fig, height=650), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-title">Revenue Heatmap: Month × Category</div>', unsafe_allow_html=True)
        heat = filtered.pivot_table(index="Category", columns="Month", values="Revenue", aggfunc="sum", fill_value=0)
        fig = px.imshow(heat, aspect="auto", color_continuous_scale=["#12071F", "#A855F7", "#F59E0B"], labels={"color": "Revenue"})
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(style_fig(fig, height=360), use_container_width=True)
    with c2:
        st.markdown('<div class="sec-title">Warehouse Revenue Breakdown</div>', unsafe_allow_html=True)
        wh = filtered.groupby("WarehouseLocation")["Revenue"].sum().reset_index()
        fig = px.bar(wh, x="WarehouseLocation", y="Revenue", color="WarehouseLocation", color_discrete_sequence=CAT_COLORS,
                     text=wh["Revenue"].apply(money))
        fig.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(style_fig(fig, height=360), use_container_width=True)
