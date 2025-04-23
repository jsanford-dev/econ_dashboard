import os
from functools import lru_cache
import time
import pandas as pd
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
        "Public Debt to GDP (%)":"GFDEGDQ188S",
        "Population Level":"POPTHM"
    }

    data = {}
    for label, series_id in series_ids.items():
        try:
            series = fred.get_series(series_id)
            latest_value = series.dropna().iloc[-1]
            latest_date = series.dropna().index[-1].strftime('%b %Y')
            info = fred.get_series_info(series_id)
            last_updated = pd.to_datetime(info['last_updated']).strftime('%d %b %Y')
            data[label] = {
                "value": round(float(latest_value), 2),
                "period": latest_date,
                "last_updated": last_updated
            }
        except Exception as e:
            data[label] = {
                "value": f"Error: {str(e)}",
                "date": "N/A"
            }

    return data

@lru_cache(maxsize=1)
def fetch_us_overview_data_cached():
    print("Fetching fresh data from FRED...")
    return fetch_us_overview_data()