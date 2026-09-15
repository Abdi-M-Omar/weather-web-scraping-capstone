# ============================================================
# Weather Web Scraping Capstone
# Streamlit Dashboard
# ============================================================

import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="Weather Web Scraping Dashboard",
    page_icon="🌤️",
    layout="wide"
)


# ============================================================
# DATABASE
# ============================================================

# weather.db is stored in the same folder as this file.
BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = BASE_DIR / "weather.db"


@st.cache_data
def load_data():
    """
    Load the cleaned weather data from the SQLite database.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    query = """
        SELECT
            city,
            local_time,
            weather,
            temperature_f,
            temperature_c
        FROM cleaned_weather
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


df = load_data()


# ============================================================
# CLEAN DATA FOR DASHBOARD
# ============================================================

# Make sure temperatures are numeric.
df["temperature_f"] = pd.to_numeric(
    df["temperature_f"],
    errors="coerce"
)

df["temperature_c"] = pd.to_numeric(
    df["temperature_c"],
    errors="coerce"
)

# Remove rows that do not contain the information needed
# for the dashboard.
df = df.dropna(
    subset=["city", "weather", "temperature_f"]
)

# Sort cities alphabetically.
df = df.sort_values("city")


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title("🌤️ Weather Web Scraping Dashboard")

st.write(
    "This dashboard explores weather data collected through "
    "the web scraping capstone project."
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")


# ----------------------------
# City filter
# ----------------------------

cities = sorted(df["city"].unique())

selected_cities = st.sidebar.multiselect(
    "Select City",
    options=cities,
    default=cities
)


# ----------------------------
# Temperature filter
# ----------------------------

minimum_temperature = int(df["temperature_f"].min())
maximum_temperature = int(df["temperature_f"].max())

temperature_range = st.sidebar.slider(
    "Temperature Range (°F)",
    min_value=minimum_temperature,
    max_value=maximum_temperature,
    value=(minimum_temperature, maximum_temperature)
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["city"].isin(selected_cities))
    & (
        df["temperature_f"].between(
            temperature_range[0],
            temperature_range[1]
        )
    )
].copy()


# ============================================================
# CHECK FILTER RESULTS
# ============================================================

if filtered_df.empty:
    st.warning(
        "No weather records match the selected filters. "
        "Please change the city or temperature range."
    )

    st.stop()


# ============================================================
# WEATHER SUMMARY
# ============================================================

st.header("Weather Summary")

column1, column2, column3 = st.columns(3)


with column1:
    st.metric(
        "Cities",
        filtered_df["city"].nunique()
    )


with column2:
    average_temperature = filtered_df["temperature_f"].mean()

    st.metric(
        "Average Temperature",
        f"{average_temperature:.1f} °F"
    )


with column3:
    st.metric(
        "Weather Conditions",
        filtered_df["weather"].nunique()
    )


# ============================================================
# VISUALIZATION 1
# TEMPERATURE BY CITY
# ============================================================

st.header("1. Temperature by City")

fig_city = px.bar(
    filtered_df.sort_values("temperature_f"),
    x="city",
    y="temperature_f",
    color="city",
    title="Temperature by City",
    labels={
        "city": "City",
        "temperature_f": "Temperature (°F)"
    }
)

fig_city.update_layout(
    xaxis_title="City",
    yaxis_title="Temperature (°F)",
    showlegend=False
)

st.plotly_chart(
    fig_city,
    use_container_width=True
)


# ============================================================
# VISUALIZATION 2
# TEMPERATURE DISTRIBUTION
# ============================================================

st.header("2. Temperature Distribution")

fig_distribution = px.histogram(
    filtered_df,
    x="temperature_f",
    nbins=15,
    title="Distribution of Temperatures",
    labels={
        "temperature_f": "Temperature (°F)"
    }
)

fig_distribution.update_layout(
    xaxis_title="Temperature (°F)",
    yaxis_title="Number of Cities"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)


# ============================================================
# VISUALIZATION 3
# WEATHER CONDITIONS
# ============================================================

st.header("3. Weather Conditions")

weather_counts = (
    filtered_df["weather"]
    .value_counts()
    .reset_index()
)

weather_counts.columns = [
    "weather",
    "count"
]

# A bar chart works better than a pie chart here because
# the dataset contains many different weather descriptions.
fig_weather = px.bar(
    weather_counts,
    x="count",
    y="weather",
    orientation="h",
    title="Weather Condition Distribution",
    labels={
        "weather": "Weather Condition",
        "count": "Number of Cities"
    }
)

fig_weather.update_layout(
    xaxis_title="Number of Cities",
    yaxis_title="Weather Condition",
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig_weather,
    use_container_width=True
)


# ============================================================
# DATA EXPLORATION
# ============================================================

st.header("Explore the Data")

st.write(
    "Use the sidebar filters to explore different cities "
    "and temperature ranges."
)

display_df = filtered_df[
    [
        "city",
        "weather",
        "temperature_f",
        "temperature_c"
    ]
].copy()

display_df.columns = [
    "City",
    "Weather",
    "Temperature (°F)",
    "Temperature (°C)"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)