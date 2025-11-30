import time
import random
import datetime as dt

import pandas as pd
import psycopg2
import plotly.express as px
import streamlit as st
from faker import Faker

# -------------------------------
# 🔄 Auto-refresh every 10 seconds
# -------------------------------
st.markdown(
    "<meta http-equiv='refresh' content='30'>",
    unsafe_allow_html=True
)

# -------------------------------
# 🎨 Page config + basic styling
# -------------------------------
st.set_page_config(
    page_title="Real-Time Sales Dashboard",
    layout="wide"
)

# Simple dark-ish theme tweaks
st.markdown(
    """
    <style>
        body { background-color: #0e1117; color: #e8e8e8; }
        .stMetric { background: #1f2933; padding: 10px; border-radius: 12px; }
        .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Real-Time Sales Analytics Dashboard")
st.markdown("Data flowing from **Kafka ➜ PostgreSQL ➜ Streamlit**")

# -------------------------------
# 🗄️ DB connection helper
# -------------------------------
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="salesdb",
        user="rajatbaranwal",
        password=""         # empty password as you said
    )

# -------------------------------
# 🧪 Generate fake rows directly into DB
#    (simulating producer for demo)
# -------------------------------
fake = Faker()
PRODUCTS = ["Laptop", "Mobile", "Headphones", "Keyboard", "Mouse"]

def generate_fake_sales(n_rows: int = 10):
    conn = get_connection()
    cur = conn.cursor()
    for _ in range(n_rows):
        product = random.choice(PRODUCTS)
        qty = random.randint(1, 5)
        price = round(random.uniform(5000, 50000), 2)
        ts = fake.date_time_this_year()
        cur.execute(
            """
            INSERT INTO sales_data (product_name, quantity, price, timestamp)
            VALUES (%s, %s, %s, %s)
            """,
            (product, qty, price, ts)
        )
    conn.commit()
    cur.close()
    conn.close()

# Button to simulate new sales
if st.button("➕ Generate 10 New Fake Sales"):
    try:
        generate_fake_sales(10)
        st.success("Inserted 10 new fake sales into `sales_data` ✅")
    except Exception as e:
        st.error(f"Error inserting fake data: {e}")

st.divider()

# -------------------------------
# 📥 Load data from PostgreSQL
# -------------------------------
@st.cache_data(ttl=5)
def load_data():
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM sales_data ORDER BY timestamp ASC;", conn)
        conn.close()
        if df.empty:
            return df
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["revenue"] = df["quantity"] * df["price"]
        df["date"] = df["timestamp"].dt.date
        df["hour"] = df["timestamp"].dt.hour
        df["month"] = df["timestamp"].dt.to_period("M").astype(str)
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data in `sales_data` yet. Run consumer / use the button above to generate some.")
    st.stop()

# -------------------------------
# 🎛 Filters (Sidebar)
# -------------------------------
st.sidebar.header("🔎 Filters")

# Product filter
products = sorted(df["product_name"].unique())
selected_products = st.sidebar.multiselect(
    "Product(s)",
    options=products,
    default=products
)

# Date range filter
min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Quantity range filter
min_qty, max_qty = int(df["quantity"].min()), int(df["quantity"].max())
qty_min, qty_max = st.sidebar.slider(
    "Quantity range",
    min_value=min_qty,
    max_value=max_qty,
    value=(min_qty, max_qty)
)

# Apply filters
filtered = df.copy()

if selected_products:
    filtered = filtered[filtered["product_name"].isin(selected_products)]

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["date"] >= start_date) & (filtered["date"] <= end_date)
    ]

filtered = filtered[
    (filtered["quantity"] >= qty_min) & (filtered["quantity"] <= qty_max)
]

if filtered.empty:
    st.warning("No data after applying filters. Adjust filters to see results.")
    st.stop()

# -------------------------------
# 📌 KPI Cards (Top Section)
# -------------------------------
total_sales = len(filtered)
total_revenue = filtered["revenue"].sum()
avg_price = filtered["price"].mean()
today = dt.date.today()
revenue_today = filtered[filtered["date"] == today]["revenue"].sum()

if not filtered.empty:
    top_product = (
        filtered.groupby("product_name")["revenue"].sum().sort_values(ascending=False).index[0]
    )
else:
    top_product = "N/A"

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("📦 Total Sales (rows)", f"{total_sales:,}")
c2.metric("💰 Total Revenue", f"₹{total_revenue:,.2f}")
c3.metric("🏷️ Avg Price", f"₹{avg_price:,.2f}")
c4.metric("🏆 Top Product", top_product)
c5.metric("📅 Revenue Today", f"₹{revenue_today:,.2f}")

st.divider()

# -------------------------------
# 📊 MAIN GRAPHS
# -------------------------------

# 1) Revenue by Product (bar)
st.subheader("🏆 Revenue by Product")
rev_by_product = (
    filtered.groupby("product_name")["revenue"].sum().reset_index().sort_values("revenue", ascending=False)
)
fig1 = px.bar(
    rev_by_product,
    x="product_name",
    y="revenue",
    color="product_name",
    title="Revenue by Product",
    text_auto=True
)
st.plotly_chart(fig1, use_container_width=True)

# 2) Daily Revenue Trend
st.subheader("📈 Daily Revenue Trend")
daily_rev = (
    filtered.groupby("date")["revenue"].sum().reset_index()
)
fig2 = px.line(
    daily_rev,
    x="date",
    y="revenue",
    markers=True,
    title="Daily Revenue (Filtered Data)"
)
st.plotly_chart(fig2, use_container_width=True)

# 3) Hourly Sales Trend
st.subheader("⏱ Hourly Sales Trend (all filtered days combined)")
hourly_rev = (
    filtered.groupby("hour")["revenue"].sum().reset_index()
)
fig3 = px.bar(
    hourly_rev,
    x="hour",
    y="revenue",
    title="Revenue by Hour of Day"
)
st.plotly_chart(fig3, use_container_width=True)

# 4) Monthly Revenue Trend
st.subheader("📅 Monthly Revenue Trend")
monthly_rev = (
    filtered.groupby("month")["revenue"].sum().reset_index()
)
fig4 = px.line(
    monthly_rev,
    x="month",
    y="revenue",
    markers=True,
    title="Monthly Revenue"
)
st.plotly_chart(fig4, use_container_width=True)

# 5) Top 10 Products by Revenue
st.subheader("🔟 Top 10 Products by Revenue")
top10 = (
    filtered.groupby("product_name")["revenue"].sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig5 = px.bar(
    top10,
    x="product_name",
    y="revenue",
    title="Top 10 Products by Revenue",
    text_auto=True
)
st.plotly_chart(fig5, use_container_width=True)

# 6) Quantity Heatmap (Product vs Date)
st.subheader("🔥 Quantity Heatmap (Product vs Date)")
qty_heat = (
    filtered.groupby(["product_name", "date"])["quantity"].sum().reset_index()
)
pivot = qty_heat.pivot(index="product_name", columns="date", values="quantity").fillna(0)
fig6 = px.imshow(
    pivot,
    aspect="auto",
    title="Quantity Heatmap (Product vs Date)",
    labels=dict(x="Date", y="Product", color="Quantity")
)
st.plotly_chart(fig6, use_container_width=True)

# 7) Price Density Curve
st.subheader("📉 Price Density (Histogram)")
fig7 = px.histogram(
    filtered,
    x="price",
    nbins=30,
    histnorm="density",
    title="Price Distribution (Density)"
)
st.plotly_chart(fig7, use_container_width=True)

st.divider()

# -------------------------------
# 📋 Latest Records Table
# -------------------------------
st.subheader("📄 Latest 30 Sales (after filters)")
st.dataframe(
    filtered.sort_values("timestamp", ascending=False).head(30),
    use_container_width=True
)

st.divider()

# -------------------------------
# 🔗 Pipeline Diagram
# -------------------------------
st.subheader("🔗 Data Pipeline Overview")
st.markdown(
    """
📦 **Data Pipeline Overview**

Python Producer → Kafka Topic (sales-topic) → Kafka Consumer  
↓  
PostgreSQL (salesdb.sales_data) → Streamlit Dashboard
"""
)