import os
import yaml
import pandas as pd

# Folder where all month folders are present
data_folder = "data"

# Dictionary to store all stock data
all_data = {}

print("Reading data from YAML files...")

# Loop through each month folder
for month_folder in os.listdir(data_folder):
    month_path = os.path.join(data_folder, month_folder)

    # Skip if it is not a folder
    if not os.path.isdir(month_path):
        continue

    # Loop through each YAML file inside the month folder
    for yaml_file in os.listdir(month_path):
        if not yaml_file.endswith(".yaml"):
            continue

        file_path = os.path.join(month_path, yaml_file)

        # Open and read the YAML file
        with open(file_path, "r") as f:
            records = yaml.safe_load(f)

        # Loop through each stock record in the file
        for record in records:
            ticker = record["Ticker"]

            # Create a new list if stock not seen before
            if ticker not in all_data:
                all_data[ticker] = []

            # Append the stock data
            all_data[ticker].append({
                "Date"  : record["date"],
                "Open"  : record["open"],
                "High"  : record["high"],
                "Low"   : record["low"],
                "Close" : record["close"],
                "Volume": record["volume"],
                "Month" : record["month"]
            })

# Create output folder to save CSV files
os.makedirs("csv_output", exist_ok=True)

print("Creating CSV files...")

# Save one CSV file per stock
for ticker, data in all_data.items():
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df.to_csv(f"csv_output/{ticker}.csv", index=False)
    print(f"  Created: {ticker}.csv")

print(f"\nDone! Total {len(all_data)} CSV files created!")