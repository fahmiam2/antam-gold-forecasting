from pathlib import Path
import sys

# Get the root directory (two levels up from the src directory)
root_directory = Path(__file__).resolve().parents[1]
sys.path.append(str(root_directory))

from typing import Dict
import yfinance as yf
import pandas as pd

class StockDataFetcher:
    def __init__(self, ticker_symbols: Dict[str, str], start_date: str, end_date: str) -> None:
        self.ticker_symbols = ticker_symbols
        self.start_date = start_date
        self.end_date = end_date

    def fetch_stock_data(self, ticker_symbol: str) -> pd.DataFrame:
        return yf.download(ticker_symbol, start=self.start_date, end=self.end_date)

    def export_to_csv(self, data: pd.DataFrame, filename: str) -> None:
        data.to_csv(filename)

    def fetch_and_export_data(self) -> None:
        for ticker_symbol, index_name in self.ticker_symbols.items():
            print(f"Fetching and exporting data for {index_name} ({ticker_symbol})...")
            data = self.fetch_stock_data(ticker_symbol)
            filename = str(root_directory) + f"/data/01_raw/{index_name}_data.csv"
            self.export_to_csv(data, filename)
            print(f"Data exported to {filename}\n")

# Define the ticker symbols and start/end dates
ticker_symbols = {
    "^GSPC": "S&P 500 Index", 
    "^IXIC": "NASDAQ Composite Index",
    "USDIDR=X": "USD to IDR Exchange Rate"
}

start_date: str = "2010-01-04"
end_date: str = "2024-04-30"

# Instantiate StockDataFetcher and fetch/export data
stock_data_fetcher = StockDataFetcher(ticker_symbols, start_date, end_date)
stock_data_fetcher.fetch_and_export_data()
