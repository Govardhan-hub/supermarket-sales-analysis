import calendar

import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#4F46E5"
PALETTE = ["#4F46E5", "#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#14B8A6"]
CURRENCY = "₹"
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ==============================
# CUSTOM CSS
# ==============================
st.markdown(
    """
    <style>
        .block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px;}
        h1 {font-weight: 800; letter-spacing: -0.5px;}
        .subtitle {color: #6B7280; margin-top: -0.6rem; margin-bottom: 1.2rem;}

        /* KPI cards */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #FFFFFF 0%, #F5F5FF 100%);
            border: 1px solid #E5E7EB;
            border-left: 5px solid #4F46E5;
            padding: 16px 18px;
            border-radius: 14px;
            box-shadow: 0 2px 8px rgba(17, 24, 39, 0.06);
        }
        div[data-testid="stMetric"] label {color: #6B7280 !important; font-weight: 600;}
        div[data-testid="stMetricValue"] {color: #111827; font-weight: 800; font-size: 1.6rem;}
        div[data-testid="stMetricValue"] > div {
            overflow: visible !important;
            text-overflow: clip !important;
            white-space: nowrap !important;
        }

        /* Tabs */
        button[data-baseweb="tab"] {font-weight: 600; font-size: 0.95rem;}

        /* Insight cards */
        .insight {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-left: 5px solid #4F46E5;
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 12px;
            color: #1F2937;
        }
        .insight b {color: #4F46E5;}

        /* Hide default footer / menu clutter */
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================
# DATA LOADING + CLEANING
# ==============================
@st.cache_data
def load_data(path: str = "supermarket.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")
    df["Customer_Type"] = df["Customer_Type"].fillna("Unknown")
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df = df.drop_duplicates()

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"])
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Month"].apply(lambda m: calendar.month_abbr[m])
    df["Day"] = df["Date"].dt.day_name()
    df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M", errors="coerce").dt.hour
    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ `supermarket.csv` not found. Place it in the same folder as `dashboard.py`.")
    st.stop()


# ==============================
# HELPERS
# ==============================
def money(x: float) -> str:
    return f"{CURRENCY}{x:,.2f}"


def style(fig, height=380, legend=False):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Inter, Segoe UI, sans-serif", size=13),
        showlegend=legend,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#EEF0F4")
    return fig


def bar(series: pd.Series, horizontal=False, color=PRIMARY, xlabel="", ylabel="", height=380):
    data = series.reset_index()
    data.columns = ["label", "value"]
    if horizontal:
        data = data.sort_values("value")
        fig = px.bar(data, x="value", y="label", orientation="h", text_auto=".3s")
    else:
        fig = px.bar(data, x="label", y="value", text_auto=".3s")
    fig.update_traces(marker_color=color, marker_line_width=0, textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis_title=xlabel, yaxis_title=ylabel)
    return style(fig, height)


def section(title: str):
    st.markdown(f"#### {title}")


# ==============================
# SIDEBAR FILTERS
# ==============================
st.sidebar.title("🎛️ Filters")
st.sidebar.caption("Slice the data — every chart updates instantly.")

min_d, max_d = df["Date"].min().date(), df["Date"].max().date()
date_range = st.sidebar.date_input("Date range", (min_d, max_d), min_value=min_d, max_value=max_d)

branches = st.sidebar.multiselect("Branch", sorted(df["Branch"].unique()), default=sorted(df["Branch"].unique()))
categories = st.sidebar.multiselect(
    "Product category", sorted(df["Product_Line"].unique()), default=sorted(df["Product_Line"].unique())
)
customers = st.sidebar.multiselect(
    "Customer type", sorted(df["Customer_Type"].unique()), default=sorted(df["Customer_Type"].unique())
)
genders = st.sidebar.multiselect("Gender", sorted(df["Gender"].dropna().unique()), default=sorted(df["Gender"].dropna().unique()))
payments = st.sidebar.multiselect(
    "Payment method", sorted(df["Payment_Method"].unique()), default=sorted(df["Payment_Method"].unique())
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
else:
    start, end = min_d, max_d

f = df[
    (df["Date"].dt.date >= start)
    & (df["Date"].dt.date <= end)
    & (df["Branch"].isin(branches))
    & (df["Product_Line"].isin(categories))
    & (df["Customer_Type"].isin(customers))
    & (df["Gender"].isin(genders))
    & (df["Payment_Method"].isin(payments))
]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(f):,}** of **{len(df):,}** transactions")
with st.sidebar.expander("⬇️ Download data"):
    st.download_button(
        "Download filtered CSV",
        f.to_csv(index=False).encode("utf-8"),
        "supermarket_filtered.csv",
        "text/csv",
        use_container_width=True,
    )

# ==============================
# HEADER
# ==============================
st.title("🛒 Supermarket Sales Dashboard")
st.markdown(
    '<p class="subtitle">Revenue, customer behaviour, product performance and time trends — all in one place.</p>',
    unsafe_allow_html=True,
)

if f.empty:
    st.warning("No data matches the selected filters. Try widening them in the sidebar.")
    st.stop()

# ==============================
# KPI ROW
# ==============================
total_rev = f["Total"].sum()
total_gross = f["Gross_Income"].sum()
gross_pct = (total_gross / total_rev * 100) if total_rev else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("💰 Total Revenue", money(total_rev))
k2.metric("📈 Gross Income", money(total_gross))
k3.metric("🧾 Transactions", f"{len(f):,}")
k4.metric("🛍️ Avg Transaction", money(f["Total"].mean()))
k5.metric("📊 Gross Margin", f"{gross_pct:.2f}%")

st.write("")

# ==============================
# TABS
# ==============================
tab_over, tab_prod, tab_cust, tab_time, tab_corr, tab_ins = st.tabs(
    ["🏬 Overview", "📦 Products", "👥 Customers", "⏰ Time Trends", "🔗 Correlation", "💡 Insights"]
)

# ---------- OVERVIEW ----------
with tab_over:
    branch_revenue = f.groupby("Branch")["Total"].sum()
    branch_profit = f.groupby("Branch")["Gross_Income"].sum()
    branch_tx = f["Branch"].value_counts()
    branch_avg = f.groupby("Branch")["Total"].mean()

    c1, c2 = st.columns(2)
    with c1:
        section("Revenue by Branch")
        st.plotly_chart(bar(branch_revenue, color="#4F46E5", xlabel="Branch", ylabel="Revenue"), use_container_width=True)
    with c2:
        section("Gross Income by Branch")
        st.plotly_chart(bar(branch_profit, color="#10B981", xlabel="Branch", ylabel="Gross Income"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        section("Transactions by Branch")
        st.plotly_chart(bar(branch_tx, color="#06B6D4", xlabel="Branch", ylabel="Transactions"), use_container_width=True)
    with c4:
        section("Average Transaction by Branch")
        st.plotly_chart(bar(branch_avg, color="#F59E0B", xlabel="Branch", ylabel="Average Transaction"), use_container_width=True)

# ---------- PRODUCTS ----------
with tab_prod:
    category_revenue = f.groupby("Product_Line")["Total"].sum()
    product_profit = f.groupby("Product_Line")["Gross_Income"].sum()
    product_quantity = f.groupby("Product_Line")["Quantity"].sum()
    product_rating = f.groupby("Product_Line")["Rating"].mean()
    product_price = f.groupby("Product_Line")["Unit_Price"].mean()
    category_cogs = f.groupby("Product_Line")["COGS"].sum()

    c1, c2 = st.columns(2)
    with c1:
        section("Revenue by Category")
        st.plotly_chart(bar(category_revenue, horizontal=True, color="#4F46E5", xlabel="Revenue"), use_container_width=True)
    with c2:
        section("Gross Income by Category")
        st.plotly_chart(bar(product_profit, horizontal=True, color="#10B981", xlabel="Gross Income"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        section("Quantity Sold by Category")
        st.plotly_chart(bar(product_quantity, horizontal=True, color="#06B6D4", xlabel="Units Sold"), use_container_width=True)
    with c4:
        section("COGS by Category")
        st.plotly_chart(bar(category_cogs, horizontal=True, color="#8B5CF6", xlabel="COGS"), use_container_width=True)

    c5, c6 = st.columns(2)
    with c5:
        section("Average Rating by Category")
        st.plotly_chart(bar(product_rating.round(2), horizontal=True, color="#F59E0B", xlabel="Average Rating"), use_container_width=True)
    with c6:
        section("Average Unit Price by Category")
        st.plotly_chart(bar(product_price.round(2), horizontal=True, color="#EC4899", xlabel="Average Unit Price"), use_container_width=True)

# ---------- CUSTOMERS ----------
with tab_cust:
    customer_rev = f.groupby("Customer_Type")["Total"].sum()
    customer_avg = f.groupby("Customer_Type")["Total"].mean()
    gender_rev = f.groupby("Gender")["Total"].sum()
    gender_avg = f.groupby("Gender")["Total"].mean()
    payment_rev = f.groupby("Payment_Method")["Total"].sum()
    payment_profit = f.groupby("Payment_Method")["Gross_Income"].sum()

    c1, c2 = st.columns(2)
    with c1:
        section("Revenue by Customer Type")
        st.plotly_chart(bar(customer_rev, color="#4F46E5", xlabel="Customer Type", ylabel="Revenue"), use_container_width=True)
    with c2:
        section("Average Transaction by Customer Type")
        st.plotly_chart(bar(customer_avg, color="#8B5CF6", xlabel="Customer Type", ylabel="Average"), use_container_width=True)
        counts = f["Customer_Type"].value_counts()
        if "Unknown" in counts.index and counts["Unknown"] < 0.05 * len(f):
            st.caption(f"⚠️ Only {counts['Unknown']} 'Unknown' transactions — interpret that bar cautiously.")

    c3, c4 = st.columns(2)
    with c3:
        section("Revenue by Gender")
        st.plotly_chart(bar(gender_rev, color="#0E7490", xlabel="Gender", ylabel="Revenue"), use_container_width=True)
    with c4:
        section("Average Transaction by Gender")
        st.plotly_chart(bar(gender_avg, color="#CA8A04", xlabel="Gender", ylabel="Average"), use_container_width=True)

    c5, c6 = st.columns(2)
    with c5:
        section("Revenue Share by Payment Method")
        fig = px.pie(
            payment_rev.reset_index(), names="Payment_Method", values="Total", hole=0.5, color_discrete_sequence=PALETTE
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(style(fig, legend=True), use_container_width=True)
    with c6:
        section("Gross Income by Payment Method")
        st.plotly_chart(bar(payment_profit, color="#EF4444", xlabel="Payment Method", ylabel="Gross Income"), use_container_width=True)

# ---------- TIME TRENDS ----------
with tab_time:
    month_rev = f.groupby(["Month", "Month_Name"])["Total"].sum().reset_index().sort_values("Month")
    day_rev = f.groupby("Day")["Total"].sum().reindex(DAY_ORDER).dropna()
    hour_rev = f.groupby("Hour")["Total"].sum()

    section("Monthly Revenue")
    fig = px.area(month_rev, x="Month_Name", y="Total", markers=True)
    fig.update_traces(line_color=PRIMARY, fillcolor="rgba(79,70,229,0.15)")
    fig.update_layout(xaxis_title="Month", yaxis_title="Revenue")
    st.plotly_chart(style(fig), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        section("Revenue by Day of Week")
        st.plotly_chart(bar(day_rev, color="#06B6D4", xlabel="Day", ylabel="Revenue"), use_container_width=True)
    with c2:
        section("Revenue by Hour")
        fig = px.line(hour_rev.reset_index(), x="Hour", y="Total", markers=True)
        fig.update_traces(line_color="#EF4444", line_width=3)
        fig.update_layout(xaxis=dict(dtick=1), xaxis_title="Hour of Day", yaxis_title="Revenue")
        st.plotly_chart(style(fig), use_container_width=True)

# ---------- CORRELATION ----------
with tab_corr:
    c1, c2 = st.columns(2)
    with c1:
        section("Quantity vs Total")
        fig = px.scatter(f, x="Quantity", y="Total", opacity=0.5, color_discrete_sequence=["#4F46E5"])
        st.plotly_chart(style(fig), use_container_width=True)
        st.metric("Correlation", f"{f['Quantity'].corr(f['Total']):.3f}")
    with c2:
        section("Unit Price vs Total")
        fig = px.scatter(f, x="Unit_Price", y="Total", opacity=0.5, color_discrete_sequence=["#10B981"])
        st.plotly_chart(style(fig), use_container_width=True)
        st.metric("Correlation", f"{f['Unit_Price'].corr(f['Total']):.3f}")

    section("Correlation Heatmap")
    num_cols = [c for c in ["Unit_Price", "Quantity", "Total", "COGS", "Gross_Income", "Rating"] if c in f.columns]
    fig = px.imshow(
        f[num_cols].corr().round(2), text_auto=True, color_continuous_scale="Purples", zmin=-1, zmax=1, aspect="auto"
    )
    st.plotly_chart(style(fig, height=450), use_container_width=True)

# ---------- INSIGHTS ----------
with tab_ins:
    top_branch = f.groupby("Branch")["Total"].sum()
    tb = top_branch.idxmax()
    tb_city = f[f["Branch"] == tb]["City"].iloc[0] if "City" in f.columns else "-"
    top_cat = f.groupby("Product_Line")["Total"].sum()
    top_qty = f.groupby("Product_Line")["Quantity"].sum()
    top_gi = f.groupby("Product_Line")["Gross_Income"].sum()
    top_rating = f.groupby("Product_Line")["Rating"].mean()
    top_cust = f.groupby("Customer_Type")["Total"].sum()
    top_pay = f.groupby("Payment_Method")["Total"].sum()
    top_month = f.groupby("Month")["Total"].sum()
    top_day = f.groupby("Day")["Total"].sum()
    top_hour = f.groupby("Hour")["Total"].sum()
    top_gender = f.groupby("Gender")["Total"].sum()

    insights = [
        f"<b>Top branch:</b> Branch {tb} ({tb_city}) leads with {money(top_branch.max())} in revenue.",
        f"<b>Top category:</b> {top_cat.idxmax()} generated the highest revenue at {money(top_cat.max())}.",
        f"<b>Most units sold:</b> {top_qty.idxmax()} with {int(top_qty.max()):,} units.",
        f"<b>Highest gross income:</b> {top_gi.idxmax()} with {money(top_gi.max())}.",
        f"<b>Best rated category:</b> {top_rating.idxmax()} with an average rating of {top_rating.max():.2f}.",
        f"<b>Top customer type:</b> {top_cust.idxmax()} contributes the most revenue.",
        f"<b>Top payment method:</b> {top_pay.idxmax()} brings in the most revenue.",
        f"<b>Top gender by revenue:</b> {top_gender.idxmax()} ({money(top_gender.max())}).",
        f"<b>Best month:</b> {calendar.month_name[int(top_month.idxmax())]} with {money(top_month.max())}.",
        f"<b>Best day:</b> {top_day.idxmax()} with {money(top_day.max())}.",
        f"<b>Peak hour:</b> {int(top_hour.idxmax())}:00 with {money(top_hour.max())}.",
        f"<b>Gross margin:</b> gross income is about {gross_pct:.2f}% of total revenue.",
    ]
    ic1, ic2 = st.columns(2)
    for i, text in enumerate(insights):
        (ic1 if i % 2 == 0 else ic2).markdown(f'<div class="insight">{text}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Built with Streamlit · Pandas · Plotly")
