import os
from functools import lru_cache
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load .env
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# connect to database
engine = create_engine(DATABASE_URL)

# series mapping
series_labels = {
    "Real GDP Growth (%)": "real_gdp_growth",
    "Real GDP Level": "real_gdp_level",
    "Inflation (PCE YoY%)": "inflation_rate",
    "Unemployment Rate (%)": "unemployment_rate",
    "10Y Treasury Yield (%)": "treasury_10y_yield",
    "Fed Funds Rate (%)": "fed_funds_rate",
    "Public Debt to GDP (%)": "public_debt_gdp",
    "Population Level": "population_level"
}

def fetch_us_overview_data():
    """
    Pulls the latest data from the database and structures it like the FRED client.
    """
    query = """
        SELECT 
            date, 
            real_gdp_growth, 
            real_gdp_level, 
            inflation_rate, 
            unemployment_rate, 
            treasury_10y_yield, 
            fed_funds_rate, 
            public_debt_gdp, 
            population_level 
        FROM us_overview_data
        WHERE date >= '2020-08-01'
        ORDER BY date DESC
    """
    df = pd.read_sql(query, engine)

    if df.empty:
        return {}

    data = {}
    for label, column in series_labels.items():
        try:
            # Drop NaNs and sort by date
            valid_data = df[['date', column]].dropna().sort_values(by='date', ascending=False)

            # If there is no valid data, set to "N/A"
            if valid_data.empty:
                data[label] = {
                    "value": "N/A",
                    "previous": "N/A",
                    "period": "N/A",
                    "last_updated": "N/A"
                }
            else:
                latest_value = valid_data.iloc[0][column]
                latest_date = valid_data.iloc[0]['date'].strftime('%b %Y')

                # Filler below  - need to feed in FRED metadata at some point
                last_updated = valid_data.iloc[0]['date'].strftime('%d %b %Y') 

                # Previous value (if exists)
                if len(valid_data) > 1:
                    previous_value = valid_data.iloc[1][column]
                else:
                    previous_value = "N/A"

                # Structure the response
                data[label] = {
                    "value": round(float(latest_value), 2) if pd.notna(latest_value) else "N/A",
                    "previous": round(float(previous_value), 2) if pd.notna(previous_value) else "N/A",
                    "period": latest_date,
                    "last_updated": last_updated
                }
        except Exception as e:
            print(f"Error fetching data for {label}: {e}")
            data[label] = {
                "value": "Error",
                "previous": "Error",
                "period": "Error",
                "last_updated": "Error"
            }

    return data

# cache response
@lru_cache(maxsize=1)
def fetch_us_overview_data_cached():
    print("📡 Fetching fresh data from the Database...")
    return fetch_us_overview_data()
