import pandas as pd
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io

class ProcessData():
    def __init__(self, df, recession):
        """Initialise ProcessData class."""
        self.df = df
        self.recession = recession

    def convert_to_dataframe(self):
        """Convert series to dataframe for convenience."""
        df = self.df
        df.index = pd.to_datetime(df.index)
        df = df.to_frame(name="data").reset_index()
        df = df.rename(columns={"index":"date"})

        if self.recession is not None:
            recession_df = self.recession.to_frame(name="recession")
            recession_df.index = pd.to_datetime(recession_df.index)
            recession_df = recession_df.reset_index().rename(
                columns={"index":"date"}
            )
            df = pd.merge(df, recession_df, on="date", how="left")
            df["recession"] = df["recession"].fillna(0)

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

    def generate_chart_buffer(self):
        """Generate a chart and return it as an in-memory buffer."""
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

        # Add recession periods
        if "recession" in self.df.columns:
            recession_periods = self.df[self.df["recession"] == 1]
            for i in range(len(recession_periods) - 1):
                start = recession_periods["date"].iloc[i]
                end = recession_periods["date"].iloc[i + 1]

                if (end - start).days <=35:
                    ax.axvspan(start, end, color='lightcoral', alpha=0.3)

        recession_patch = mpatches.Patch(
            color='lightcoral', alpha=0.3, label='Recession'
        )

        ax.set_title("Change in US Non-Farm Payrolls (Total Private)")
        ax.set_ylabel("Thousands of Persons, Seasonally adjusted")
        
        ax.legend(handles=ax.get_legend_handles_labels()[0] + [recession_patch])
        ax.tick_params(axis='x', labelrotation=45)

        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        return buf


