import yfinance as yf
import pandas as pd
import os
from dotenv import load_dotenv
from udf_gsheet import fetch_gsheet_as_dataframe, filter_dataframe_columns
from stocks_aggregations import group_by_stock

def test_fetch_yfinance_history():
    """
    Test fetching historical data for a sample ticker using yfinance directly.
    """
    ticker = "AAPL"
    yf_ticker = yf.Ticker(ticker)
    hist_df = yf_ticker.history(period="1mo", interval="1d")
    print(f"Fetched {len(hist_df)} rows for {ticker} (last month, daily):")
    print(hist_df.head())
    assert not hist_df.empty, "Should fetch at least one row of data."
    assert "Close" in hist_df.columns, "Expected 'Close' column in data."
    assert pd.api.types.is_numeric_dtype(hist_df["Close"]), "Close column should be numeric."

def test_fetch_and_aggregate_and_yfinance():
    """
    Test: Read Google Sheet, aggregate by stock, and fetch yfinance data for each stock.
    """
    load_dotenv()
    url = os.environ.get("GOOGLE_SHEET_CSV_URL")
    assert url, "GOOGLE_SHEET_CSV_URL must be set in .env for testing."
    df = fetch_gsheet_as_dataframe(url)
    filtered_df = filter_dataframe_columns(df, ["Stock", "Cantidad_Comprada"], n_rows=None)
    grouped_df = group_by_stock(filtered_df)
    print("Aggregated stocks from sheet:")
    print(grouped_df)
    for stock in grouped_df["Stock"]:
        # Clean ticker: if there's a colon, use only what's after it
        cleaned_stock = stock.split(":")[-1] if ":" in stock else stock
        print(f"\nFetching yfinance data for: {cleaned_stock} (original: {stock})")
        try:
            yf_ticker = yf.Ticker(cleaned_stock)
            hist_df = yf_ticker.history(period="1mo", interval="1d")
            print(f"{cleaned_stock}: {len(hist_df)} rows fetched.")
            assert not hist_df.empty, f"No data for {cleaned_stock}"
        except Exception as e:
            print(f"Error fetching {cleaned_stock}: {e}")

if __name__ == "__main__":
    test_fetch_yfinance_history()
    print("yfinance fetch test passed.")
    print("\n--- Aggregation and yfinance test ---")
    test_fetch_and_aggregate_and_yfinance()
    print("Google Sheet aggregation + yfinance test completed.")
