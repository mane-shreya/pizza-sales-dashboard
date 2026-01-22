import pandas as pd
import streamlit as st
import plotly.express as px
import base64
import os

from src.data_loader import load_pizza_data
from src.kpis import (
    total_revenue,
    total_orders,
    total_pizzas_sold,
    avg_order_value
)

# ---------------------------------
# PAGE CONFIG (FIRST LINE)
# ---------------------------------
st.set_page_config(
    page_title="Pizza Sales Dashboard",
    layout="wide",
    page_icon="🍕"
)

# ---------------------------------
# ANIMATED GIF BACKGROUND (SAFE)
# ---------------------------------
def set_gif_background(gif_file):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(base_dir, "assets", gif_file)

    with open(gif_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/gif;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        [data-testid="stSidebar"] {{
            background-color: rgba(2,6,23,0.95);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_gif_background("bg.gif")

# ---------------------------------
# LOAD DATA
# ---------------------------------
data = load_pizza_data()

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
st.sidebar.title("🍕 Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [data["order_date"].min(), data["order_date"].max()]
)

category_filter = st.sidebar.multiselect(
    "Pizza Category",
    options=sorted(data["pizza_category"].unique()),
    default=sorted(data["pizza_category"].unique())
)

size_filter = st.sidebar.multiselect(
    "Pizza Size",
    options=sorted(data["pizza_size"].unique()),
    default=sorted(data["pizza_size"].unique())
)

# ---------------------------------
# APPLY FILTERS
# ---------------------------------
filtered_data = data[
    (data["order_date"] >= pd.to_datetime(date_range[0])) &
    (data["order_date"] <= pd.to_datetime(date_range[1])) &
    (data["pizza_category"].isin(category_filter)) &
    (data["pizza_size"].isin(size_filter))
]

# ---------------------------------
# HEADER (LOGO + TITLE)
# ---------------------------------
h1, h2 = st.columns([1,6])

with h1:
    st.image("assets/logo.png", width=70)

with h2:
    st.markdown("""
    <h2 style="color:#facc15;margin-bottom:0;">
        Pizza Sales Dashboard
    </h2>
    <p style="color:#a855f7;margin-top:0;">
        Live Sales & Customer Analytics
    </p>
    """, unsafe_allow_html=True)

# ---------------------------------
# KPI ROW
# ---------------------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("💰 Revenue", f"${total_revenue(filtered_data):,.0f}")
with k2:
    st.metric("🧾 Orders", total_orders(filtered_data))
with k3:
    st.metric("🍕 Pizzas Sold", total_pizzas_sold(filtered_data))
with k4:
    st.metric("📈 Avg Order", f"${avg_order_value(filtered_data):,.2f}")

# ---------------------------------
# ROW 1 CHARTS
# ---------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    cat_sales = (
        filtered_data.groupby("pizza_category")["total_price"]
        .sum().reset_index()
    )
    fig = px.pie(
        cat_sales,
        names="pizza_category",
        values="total_price",
        hole=0.6,
        color_discrete_sequence=[
            "#a855f7", "#14b8a6", "#facc15",
            "#ec4899", "#fb923c"
        ]
    )
    fig.update_layout(height=260, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    monthly = (
        filtered_data.groupby(
            filtered_data["order_date"].dt.to_period("M")
        )["total_price"]
        .sum().reset_index()
    )
    monthly["order_date"] = monthly["order_date"].astype(str)
    fig = px.line(monthly, x="order_date", y="total_price", markers=True)
    fig.update_traces(line_color="#14b8a6")
    fig.update_layout(height=260, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c3:
    filtered_data["order_hour"] = pd.to_datetime(
        filtered_data["order_time"].astype(str),
        errors="coerce"
    ).dt.hour
    hourly = (
        filtered_data.groupby("order_hour")["total_price"]
        .sum().reset_index()
    )
    fig = px.bar(
        hourly,
        x="order_hour",
        y="total_price",
        color="order_hour",
        color_discrete_sequence=[
            "#a855f7", "#14b8a6", "#facc15",
            "#ec4899", "#fb923c"
        ]
    )
    fig.update_layout(
        height=260,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# ROW 2 CHARTS
# ---------------------------------
b1, b2 = st.columns(2)

with b1:
    top = (
        filtered_data.groupby("pizza_name")["total_price"]
        .sum().sort_values(ascending=False)
        .head(10).reset_index()
    )
    fig = px.bar(
        top,
        x="total_price",
        y="pizza_name",
        orientation="h",
        color="pizza_name",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(
        height=280,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

with b2:
    filtered_data["order_day"] = filtered_data["order_date"].dt.day_name()
    day = (
        filtered_data.groupby("order_day")["total_price"]
        .sum()
        .reindex([
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ])
        .reset_index()
    )
    fig = px.bar(
        day,
        x="order_day",
        y="total_price",
        color="order_day",
        color_discrete_sequence=[
            "#14b8a6", "#a855f7", "#facc15",
            "#ec4899", "#fb923c", "#22c55e", "#38bdf8"
        ]
    )
    fig.update_layout(
        height=280,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)
