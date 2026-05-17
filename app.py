import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📈 Nifty 50 Stock Performance Dashboard")

csv_folder = "csv_output"

# Load all stock summary
summary = []
for file in os.listdir(csv_folder):
    if not file.endswith(".csv"): continue
    ticker = file.replace(".csv", "")
    df = pd.read_csv(os.path.join(csv_folder, file))
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    first = df["Close"].iloc[0]
    last  = df["Close"].iloc[-1]
    ret   = ((last - first) / first) * 100
    summary.append({"Ticker": ticker, "Yearly Return": round(ret, 2)})

df_summary = pd.DataFrame(summary).sort_values("Yearly Return", ascending=False)

# --- Section 1: Market Overview ---
st.header("🌍 Market Overview")
col1, col2, col3 = st.columns(3)
green = df_summary[df_summary["Yearly Return"] > 0]
red   = df_summary[df_summary["Yearly Return"] <= 0]
col1.metric("Total Stocks", len(df_summary))
col2.metric("Green Stocks 📈", len(green))
col3.metric("Red Stocks 📉", len(red))

# --- Section 2: Top 10 Green & Red ---
st.header("🏆 Top 10 Green & Red Stocks")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Green Stocks 💚")
    st.dataframe(df_summary.head(10), use_container_width=True)

with col2:
    st.subheader("Top 10 Red Stocks ❤️")
    st.dataframe(df_summary.tail(10), use_container_width=True)

# --- Section 3: Show Charts ---
st.header("📊 Analysis Charts")

charts = {
    "Top 10 Green Stocks"         : "top10_green.png",
    "Top 10 Red Stocks"           : "top10_red.png",
    "Top 10 Volatile Stocks"      : "top10_volatility.png",
    "Cumulative Return (Top 5)"   : "cumulative_return.png",
    "Sector Performance"          : "sector_performance.png",
    "Monthly Gainers & Losers"    : "monthly_gainers_losers.png",
}

for title, img in charts.items():
    if os.path.exists(img):
        st.subheader(title)
        st.image(img, use_container_width=True)

# --- Section 4: Individual Stock View ---
st.header("🔍 Individual Stock Analysis")
ticker_list = sorted([f.replace(".csv","") for f in os.listdir(csv_folder) if f.endswith(".csv")])
selected = st.selectbox("Select a Stock", ticker_list)

df_stock = pd.read_csv(os.path.join(csv_folder, f"{selected}.csv"))
df_stock["Date"] = pd.to_datetime(df_stock["Date"])
df_stock = df_stock.sort_values("Date")

st.line_chart(df_stock.set_index("Date")["Close"])
st.dataframe(df_stock.tail(10), use_container_width=True)