import pandas as pd
import os

# Folder where CSV files are stored
input_folder = "csv_output"

print("Starting Data Cleaning...")

for file in os.listdir(input_folder):
    if not file.endswith(".csv"):
        continue

    file_path = os.path.join(input_folder, file)
    df = pd.read_csv(file_path)

    # Step 1: Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    if before != after:
        print(f"  {file}: Removed {before - after} duplicate rows")

    # Step 2: Remove rows where any value is missing
    df = df.dropna()

    # Step 3: Make sure Date column is in correct format
    df["Date"] = pd.to_datetime(df["Date"])

    # Step 4: Sort by Date (oldest first)
    df = df.sort_values("Date").reset_index(drop=True)

    # Step 5: Make sure numeric columns are correct type
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Step 6: Remove rows where High < Low (bad data)
    df = df[df["High"] >= df["Low"]]

    # Save cleaned data back to same file
    df.to_csv(file_path, index=False)

print("\nDone! All 50 CSV files cleaned successfully!")