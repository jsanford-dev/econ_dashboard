import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from fredapi import Fred
import pandas as pd
from datetime import datetime

from backend.app.db.models.us_models import USOverviewData

# Load environment variables
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Connect to the database
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Initialize the FRED client
fred = Fred(api_key=FRED_API_KEY)

model_mapping = {
    "us_overview_data": {
        "model": USOverviewData,
        "series_ids": {
            "real_gdp_growth": "A191RL1Q225SBEA",
            "real_gdp_level": "GDPC1",
            "inflation_rate": "DPCCRV1Q225SBEA",
            "unemployment_rate": "UNRATE",
            "treasury_10y_yield": "GS10",
            "fed_funds_rate": "FEDFUNDS",
            "public_debt_gdp": "GFDEGDQ188S",
            "population_level": "POPTHM"
        }
    }
}

# === Insertion Logic ===
def fetch_and_insert(model_name):
    """Fetches data from FRED and inserts it into the database."""
    model_info = model_mapping.get(model_name)
    if not model_info:
        raise ValueError(f"No mapping found for model: {model_name}")

    model = model_info["model"]
    series_ids = model_info["series_ids"]

    data_frames = []

    # Fetch each series and merge into DataFrame
    for key, series_id in series_ids.items():
        print(f"Fetching {key} from FRED...")
        data = fred.get_series(series_id)
        df = pd.DataFrame(data, columns=[key])
        df.index.name = 'date'
        df.reset_index(inplace=True)
        data_frames.append(df)

    # Merge all data into a single DataFrame
    merged_data = data_frames[0]
    for df in data_frames[1:]:
        merged_data = pd.merge(merged_data, df, on='date', how='outer')

    # Insert into database
    for _, row in merged_data.iterrows():
        instance = model(
            date=row['date'],
            **{key: row.get(key) for key in series_ids}
        )
        session.add(instance)

    session.commit()
    print(f"Data successfully inserted into {model_name}.")

# === Run the Insertion ===
if __name__ == "__main__":
    fetch_and_insert("us_overview_data")