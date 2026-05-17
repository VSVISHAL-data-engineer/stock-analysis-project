import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os

csv_folder = "csv_output"
summary = []

for file in os.listdir(csv_folder):
    if not file.endswith(".csv"):
        continue
    ticker = file.replace(".csv", "")
    df = pd.read_csv(os.path.join(csv_folder, file))
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    first_close = df["Close"].iloc[0]
    last_close = df["Close"].iloc[-1]
    yearly_return = ((last_close - first_close) / first_close) * 100
    summary.append({"Ticker": ticker, "Yearly Return": round(yearly_return, 2)})

df_summary = pd.DataFrame(summary).sort_values("Yearly Return", ascending=False)

# --- ANALYSIS 1: Top 10 Green & Red ---
top10_green = df_summary.head(10)
top10_red = df_summary.tail(10)
print("Top 10 Green Stocks:"); print(top10_green.to_string(index=False))
print("\nTop 10 Red Stocks:"); print(top10_red.to_string(index=False))

plt.figure(figsize=(12,5))
plt.bar(top10_green["Ticker"], top10_green["Yearly Return"], color="green")
plt.title("Top 10 Green Stocks"); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig("top10_green.png"); print("Saved: top10_green.png")

plt.figure(figsize=(12,5))
plt.bar(top10_red["Ticker"], top10_red["Yearly Return"], color="red")
plt.title("Top 10 Red Stocks"); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig("top10_red.png"); print("Saved: top10_red.png")

# --- ANALYSIS 2: Volatility ---
volatility_data = []
for file in os.listdir(csv_folder):
    if not file.endswith(".csv"): continue
    ticker = file.replace(".csv", "")
    df = pd.read_csv(os.path.join(csv_folder, file))
    df["Daily Return"] = df["Close"].pct_change()
    volatility_data.append({"Ticker": ticker, "Volatility": round(df["Daily Return"].std()*100, 4)})

df_vol = pd.DataFrame(volatility_data).sort_values("Volatility", ascending=False)
top10_vol = df_vol.head(10)
plt.figure(figsize=(12,5))
plt.bar(top10_vol["Ticker"], top10_vol["Volatility"], color="orange")
plt.title("Top 10 Most Volatile Stocks"); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig("top10_volatility.png"); print("Saved: top10_volatility.png")

# --- ANALYSIS 3: Cumulative Return ---
top5 = df_summary.head(5)["Ticker"].tolist()
plt.figure(figsize=(14,6))
for ticker in top5:
    df = pd.read_csv(os.path.join(csv_folder, f"{ticker}.csv"))
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df["Cumulative Return"] = ((1 + df["Close"].pct_change()).cumprod() - 1) * 100
    plt.plot(df["Date"], df["Cumulative Return"], label=ticker)
plt.title("Cumulative Return - Top 5 Stocks")
plt.legend(); plt.tight_layout()
plt.savefig("cumulative_return.png"); print("Saved: cumulative_return.png")

# --- ANALYSIS 4: Sector Performance ---
df_sector = pd.read_csv("Sector_data - Sheet1.csv")
# Extract ticker after colon
df_sector["Ticker"] = df_sector["Symbol"].str.split(":").str[-1].str.strip()
df_summary["Ticker"] = df_summary["Ticker"].str.strip()
df_merged = pd.merge(df_summary, df_sector, on="Ticker", how="inner")
sector_perf = df_merged.groupby("sector")["Yearly Return"].mean().reset_index()
sector_perf = sector_perf.sort_values("Yearly Return", ascending=False)
print("\nSector Performance:"); print(sector_perf.to_string(index=False))
colors = ["green" if x >= 0 else "red" for x in sector_perf["Yearly Return"]]
plt.figure(figsize=(14,6))
plt.bar(sector_perf["sector"], sector_perf["Yearly Return"], color=colors)
plt.title("Average Yearly Return by Sector"); plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.savefig("sector_performance.png"); print("Saved: sector_performance.png")

print("\nAll Analysis Done! Check PNG files!")# --- ANALYSIS 5: Monthly Top 5 Gainers & Losers ---
import calendar

all_monthly = []

for file in os.listdir(csv_folder):
    if not file.endswith(".csv"): continue
    ticker = file.replace(".csv", "")
    df = pd.read_csv(os.path.join(csv_folder, file))
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")
    
    for month, group in df.groupby("Month"):
        group = group.sort_values("Date")
        first = group["Close"].iloc[0]
        last = group["Close"].iloc[-1]
        monthly_return = ((last - first) / first) * 100
        all_monthly.append({
            "Ticker": ticker,
            "Month": str(month),
            "Monthly Return": round(monthly_return, 2)
        })

df_monthly = pd.DataFrame(all_monthly)
months = sorted(df_monthly["Month"].unique())
n_months = len(months)
n_cols = 3
n_rows = (n_months + n_cols - 1) // n_cols
fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, n_rows * 4))
axes = axes.flatten()

for i, month in enumerate(months):
    month_df = df_monthly[df_monthly["Month"] == month]
    month_df = month_df.sort_values("Monthly Return", ascending=False)
    
    top5 = month_df.head(5)
    bot5 = month_df.tail(5)
    combined = pd.concat([top5, bot5])
    colors = ["green" if x >= 0 else "red" for x in combined["Monthly Return"]]
    
    axes[i].bar(combined["Ticker"], combined["Monthly Return"], color=colors)
    axes[i].set_title(f"{month}")
    axes[i].tick_params(axis="x", rotation=45)

plt.suptitle("Monthly Top 5 Gainers & Losers", fontsize=16)
plt.tight_layout()
plt.savefig("monthly_gainers_losers.png")
print("Saved: monthly_gainers_losers.png")
print("\nAll Done!")