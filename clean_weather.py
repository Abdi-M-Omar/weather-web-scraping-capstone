from pathlib import Path

import pandas as pd


# -----------------------------
# File paths
# -----------------------------
DATA_DIR = Path("data")

RAW_FILE = DATA_DIR / "raw_weather.csv"
CLEAN_FILE = DATA_DIR / "cleaned_weather.csv"


# -----------------------------
# Load raw CSV
# -----------------------------
df = pd.read_csv(RAW_FILE)


# -----------------------------
# Show data before cleaning
# -----------------------------
print("BEFORE CLEANING")
print(df.head())

print("\nShape:")
print(df.shape)

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())


# -----------------------------
# Clean duplicate rows
# -----------------------------
df = df.drop_duplicates()


# -----------------------------
# Remove rows missing important data
# -----------------------------
df = df.dropna(
    subset=[
        "city",
        "temperature",
    ]
)


# -----------------------------
# Clean whitespace
# -----------------------------
text_columns = [
    "city",
    "local_time",
    "weather",
    "temperature",
]

for column in text_columns:
    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
    )


# -----------------------------
# Clean city names
# -----------------------------
# Remove the * symbol that appears next to some cities
df["city"] = (
    df["city"]
    .str.replace("*", "", regex=False)
    .str.strip()
)


# -----------------------------
# Convert Fahrenheit temperature
# into a numeric column
# -----------------------------
df["temperature_f"] = (
    df["temperature"]
    .str.replace("°F", "", regex=False)
    .str.replace("°", "", regex=False)
    .str.strip()
)

df["temperature_f"] = pd.to_numeric(
    df["temperature_f"],
    errors="coerce",
)


# Remove malformed temperature values
df = df.dropna(
    subset=["temperature_f"]
)


# -----------------------------
# Create Celsius temperature
# -----------------------------
df["temperature_c"] = (
    (df["temperature_f"] - 32)
    * 5
    / 9
).round(1)


# -----------------------------
# Sort cities alphabetically
# -----------------------------
df = df.sort_values(
    by="city"
)


# -----------------------------
# Show data after cleaning
# -----------------------------
print("\nAFTER CLEANING")
print(df.head())

print("\nShape:")
print(df.shape)

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())


# -----------------------------
# Save cleaned data
# -----------------------------
df.to_csv(
    CLEAN_FILE,
    index=False,
)

print(
    "\nCleaned data saved to:",
    CLEAN_FILE,
)