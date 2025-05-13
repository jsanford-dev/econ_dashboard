from sqlalchemy import Column, String, Float, Date, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class USOverviewData(Base):
    __tablename__ = 'us_overview_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, index=True)
    real_gdp_growth = Column(Float, nullable=True)         # Real GDP Growth (%)
    real_gdp_level = Column(Float, nullable=True)          # Real GDP Level
    inflation_rate = Column(Float, nullable=True)          # Inflation (PCE YoY%)
    unemployment_rate = Column(Float, nullable=True)       # Unemployment Rate (%)
    treasury_10y_yield = Column(Float, nullable=True)      # 10Y Treasury Yield (%)
    fed_funds_rate = Column(Float, nullable=True)          # Fed Funds Rate (%)
    public_debt_gdp = Column(Float, nullable=True)         # Public Debt to GDP (%)
    population_level = Column(Float, nullable=True)        # Population Level