import os
from dotenv import load_dotenv
from fredapi import Fred

# Load API from .env
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

fred = Fred(api_key=FRED_API_KEY)

def fetch_us_overview_data():
    series_ids = {
        "Real GDP": "A191RL1Q225SBEA",
        "Inflation (CPI YoY%)": "FPCPITOTLZGUSA",
        "Unemployment Rate (%)": "UNRATE",
        "10Y Treasury Yield (%)": "GS10",
        "Fed Funds Rate (%)": "FEDFUNDS"
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