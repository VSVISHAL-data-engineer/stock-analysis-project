import os
import pandas as pd
from sqlalchemy import create_engine, text

# MySQL connection details
user     = "root"
password = 1234 # உன் MySQL password
host     = "localhost"
database = "stock_db"

# Connect to MySQL (without database first)
engine_base = create_engine(
    f"mysql+mysqlconnector://{user}:{password}@{host}"
)

# Create database if not exists
with engine_base.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS stock_db"))
    print("Database 'stock_db' created!")

# Now connect to stock_db
engine = create_engine(
    f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
)

# Load all CSV files into MySQL
csv_folder = "csv_output"

for file in os.listdir(csv_folder):
    if not file.endswith(".csv"):
        continue

    ticker     = file.replace(".csv", "")
    file_path  = os.path.join(csv_folder, file)
    df         = pd.read_csv(file_path)

    # Upload to MySQL table
    df.to_sql(
        name      = ticker.lower(),
        con       = engine,
        if_exists = "replace",
        index     = False
    )
    print(f"  Uploaded: {ticker}")

print("\nDone! All 50 stocks uploaded to MySQL!")