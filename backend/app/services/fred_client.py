import os
from dotenv import load_dotenv
from fredapi import Fred

# Load API from .env
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

fred = Fred(api_key=FRED_API_KEY)

def fetch_labour_data():
    # FRED series IDs for labor market indicators
    series_ids = {
        "Total Nonfarm Payrolls": "PAYEMS",            # Total Nonfarm Payrolls
        "unemployment Rate": "UNRATE",                 # Unemployment Rate
        "participation rate": "CIVPART"                # Labor Force Participation Rate
    }

    data = {}
    for label, series_id in series_ids.items():
        try:
            latest_value = fred.get_series(series_id).iloc[-1]  # Get most recent value
            data[label] = round(float(latest_value), 2)
        except Exception as e:
            data[label] = f"Error: {str(e)}"

    return data