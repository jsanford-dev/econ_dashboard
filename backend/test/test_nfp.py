import os
import pandas as pd
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from fredapi import Fred
from dotenv import load_dotenv

class ProcessData():
    def __init__(self, df):
        """Initialise ProcessData class."""
        self.df = df

    def convert_to_dataframe(self):
        """Convert series to dataframe for convenience."""
        df = self.df
        df.index.name = 'date'
        df.index = pd.to_datetime(df.index)
        df = df.to_frame(name="data").reset_index()
        return df
    
    def calculate_bollinger_bands(
            self, 
            deviations=2, 
            months=120, 
            roll=3,
            hard_cutoff = pd.Timestamp("2020-08-01") #Avoids COVID-19 noise
        ):
        """
        Calculates bollinger bands to identify statistical
        outliers in underlying data.
        """
        # Filter dates
        df = self.df
        recent_date = df["date"].max()
        month_cutoff = recent_date - relativedelta(months=months)
        final_cuttoff = max(month_cutoff, hard_cutoff)

        df = df[df["date"] >= final_cuttoff].copy()

        # Calculate the change in series
        df["change"] = df["data"].diff()

        # Calculate moving averages
        df["mean_roll"] = (df["change"].rolling(roll).mean())

        # Calculate rolling standard deviation
        df["stdev_roll"] = (df["change"].rolling(roll).std(ddof=0))

        # Calculate Bollinger bands
        df["upper_bol"] = (df["mean_roll"] + (df["stdev_roll"] * deviations))
        df["lower_bol"] = (df["mean_roll"] - (df["stdev_roll"] * deviations))

        return df

    def plot_data(self):
        """Plot processed data."""
        self.df = self.convert_to_dataframe()
        rolling_months = 6 # Number of months for rolling averages
        self.df = self.calculate_bollinger_bands(
            deviations=2, months=120, roll=rolling_months
        ).dropna()
        
        # Plot data
        fig, ax = plt.subplots()
        ax.plot(self.df["date"], self.df["change"], label="Change")

        ax.plot(
            self.df["date"],
            self.df["mean_roll"],
            label=f"Rolling Mean ({rolling_months} months)"
        )

        ax.fill_between(
            self.df["date"],
            self.df["upper_bol"],
            self.df["lower_bol"],
            label="Bollinger Bands",
            color="lightgrey"
        )

        ax.set_title("Change in US Non-Farm Payrolls (Total Private)")
        ax.set_ylabel("Thousands of Persons, Seasonally adjusted")
        ax.legend()
        ax.tick_params(axis='x', labelrotation=45)
        
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    # Load FRED API
    load_dotenv()
    api_key = os.getenv("FRED_API_KEY")
    fred = Fred(api_key=api_key)
    data = fred.get_series('USPRIV')
    ProcessData(data).plot_data()


