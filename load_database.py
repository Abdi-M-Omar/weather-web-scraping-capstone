from pathlib import Path
import sqlite3

import pandas as pd


# -----------------------------
# File paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

RAW_CSV = DATA_DIR / "raw_weather.csv"
CLEAN_CSV = DATA_DIR / "cleaned_weather.csv"

DATABASE_FILE = BASE_DIR / "weather.db"


# -----------------------------
# Load CSV files into Pandas
# -----------------------------
raw_df = pd.read_csv(RAW_CSV)
clean_df = pd.read_csv(CLEAN_CSV)


print("Raw weather data:")
print(raw_df.head())
print("\nRaw shape:", raw_df.shape)

print("\nCleaned weather data:")
print(clean_df.head())
print("\nCleaned shape:", clean_df.shape)


# -----------------------------
# Open SQLite database
# -----------------------------
connection = sqlite3.connect(DATABASE_FILE)


# -----------------------------
# Save each CSV as a separate table
# -----------------------------
raw_df.to_sql(
    "raw_weather",
    connection,
    if_exists="replace",
    index=False,
)

clean_df.to_sql(
    "cleaned_weather",
    connection,
    if_exists="replace",
    index=False,
)


# -----------------------------
# Verify tables were created
# -----------------------------
cursor = connection.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
""")

tables = cursor.fetchall()

print("\nTables created in weather.db:")

for table in tables:
    print(table[0])


# -----------------------------
# Verify row counts
# -----------------------------
cursor.execute("SELECT COUNT(*) FROM raw_weather;")
raw_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM cleaned_weather;")
clean_count = cursor.fetchone()[0]

print("\nRow counts:")
print("raw_weather:", raw_count)
print("cleaned_weather:", clean_count)


# -----------------------------
# Close database
# -----------------------------
connection.close()

print("\nDatabase saved to:", DATABASE_FILE)