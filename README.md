# Weather Web Scraping Capstone

This project is a web scraping capstone project that collects weather data from the Weather Around the World website.

The project uses Selenium for web scraping, Pandas for data cleaning and transformation, SQLite for database storage, and Streamlit for interactive data visualization.

## Project Goals

The goal of this project is to:

- Scrape weather data from the web using Selenium.
- Save the raw scraped data to a CSV file.
- Load the raw data into a Pandas DataFrame.
- Clean missing, duplicate, and malformed data.
- Transform temperature data for analysis.
- Save the cleaned data to a CSV file.
- Store the cleaned data in a SQLite database.
- Query the weather data.
- Create an interactive Streamlit dashboard.

## Technologies

- Python
- Selenium
- Pandas
- SQLite
- Streamlit

## Project Structure

```text
weather-web-scraping-capstone/
├── data/
│   ├── raw_weather.csv
│   └── cleaned_weather.csv
├── scrape_weather.py
├── clean_weather.py
├── requirements.txt
└── README.md