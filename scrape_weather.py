from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# -----------------------------
# File paths
# -----------------------------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

RAW_FILE = DATA_DIR / "raw_weather.csv"


# -----------------------------
# Start Chrome
# -----------------------------
options = webdriver.ChromeOptions()

# Do not wait for every ad/image on the page to finish loading
options.page_load_strategy = "eager"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Stop Selenium from waiting forever if the website is slow
driver.set_page_load_timeout(30)

url = "https://www.timeanddate.com/weather/"

weather_data = []

try:
    try:
        driver.get(url)

    except TimeoutException:
        print(
            "Page load timed out, "
            "continuing with content already loaded..."
        )

    # Wait until the weather table appears
    rows = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "table tbody tr")
        )
    )

    print("Table rows found:", len(rows))

    # Each visual row can contain multiple cities
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")

        if len(cells) < 4:
            continue

        # Each city uses four cells:
        # city | local time | weather | temperature
        for start in range(0, len(cells), 4):
            group = cells[start:start + 4]

            if len(group) < 4:
                continue

            city = group[0].text.strip()
            local_time = group[1].text.strip()
            weather = group[2].text.strip()
            temperature = group[3].text.strip()

            # Weather description may be stored in an image
            if not weather:
                images = group[2].find_elements(
                    By.TAG_NAME,
                    "img"
                )

                if images:
                    weather = (
                        images[0].get_attribute("title")
                        or images[0].get_attribute("alt")
                        or ""
                    ).strip()

            # Skip incomplete rows
            if not city or not temperature:
                continue

            weather_data.append(
                {
                    "city": city,
                    "local_time": local_time,
                    "weather": weather,
                    "temperature": temperature,
                }
            )

finally:
    driver.quit()


# -----------------------------
# Create Pandas DataFrame
# -----------------------------
df = pd.DataFrame(
    weather_data,
    columns=[
        "city",
        "local_time",
        "weather",
        "temperature",
    ],
)

# Remove duplicate rows
df = df.drop_duplicates()


# -----------------------------
# Save raw data to CSV
# -----------------------------
df.to_csv(RAW_FILE, index=False)


# -----------------------------
# Display results
# -----------------------------
print("\nRaw weather data:")
print(df.head())

print("\nRows scraped:", len(df))
print("Saved to:", RAW_FILE)