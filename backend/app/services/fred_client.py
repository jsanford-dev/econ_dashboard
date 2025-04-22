import os
from functools import lru_cache
import time
from dotenv import load_dotenv
from fredapi import Fred

# Load API from .env
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

fred = Fred(api_key=FRED_API_KEY)

def fetch_us_overview_data():
    series_ids = {
        "Real GDP Growth (%)": "A191RL1Q225SBEA",
        "Real GDP Level":"GDPC1",
        "Inflation (CPI YoY%)": "FPCPITOTLZGUSA",
        "Unemployment Rate (%)": "UNRATE",
        "10Y Treasury Yield (%)": "GS10",
        "Fed Funds Rate (%)": "FEDFUNDS",
        "Total Public Debt to GDP (%)":"GFDEGDQ188S",
        "Population Level ('000s)":"CNP16OV"
    }

    data = {}
    for label, series_ids in series_ids.items():
        try:
            series = fred.get_series(series_ids)
            latest_value = series.dropna().iloc[-1]
            data[label] = round(float(latest_value), 2)
        except Exception as e:
            data[label] = f"Error: {str(e)}"

    return data

@lru_cache(maxsize=1)
def fetch_us_overview_data_cached():
    print("Fetching fresh data from FRED...")
    return fetch_us_overview_data()