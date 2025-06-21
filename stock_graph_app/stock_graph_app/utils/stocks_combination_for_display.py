import yfinance as yf
import pandas as pd
from typing import List

def clean_ticker(ticker: str) -> str:
    """Remove prefix before colon, if present."""
    return ticker.split(":")[-1] if ":" in ticker else ticker


def fetch_and_aggregate_stocks(stock_list: List[str], period="1mo", interval="1d") -> pd.DataFrame:
    """
    Fetch historical data for a list of stock tickers (cleaned), return aggregation summary.
    Args:
        stock_list (List[str]): List of stock tickers (possibly with prefixes)
        period (str): yfinance period
        interval (str): yfinance interval
    Returns:
        pd.DataFrame: DataFrame with columns ['Stock', 'Count', 'LastClose']
    """
    summary = []
    for stock in stock_list:
        ticker = clean_ticker(stock)
        try:
            yf_ticker = yf.Ticker(ticker)
            hist_df = yf_ticker.history(period=period, interval=interval)
            last_close = hist_df['Close'].iloc[-1] if not hist_df.empty else None
            summary.append({
                'Stock': ticker,
                'Count': len(hist_df),
                'LastClose': last_close
            })
        except Exception as e:
            summary.append({
                'Stock': ticker,
                'Count': 0,
                'LastClose': None,
                'Error': str(e)
            })
    return pd.DataFrame(summary)


def fetch_all_stocks_close_by_date(stock_list: List[str], period="1mo", interval="1d") -> pd.DataFrame:
    """
    Fetch historical Close prices for all stocks, combine into a single table by Date.
    Args:
        stock_list (List[str]): List of stock tickers (possibly with prefixes)
        period (str): yfinance period
        interval (str): yfinance interval
    Returns:
        pd.DataFrame: DataFrame with Date as index and each stock as a column of Close prices.
    """
    closes = {}
    for stock in stock_list:
        ticker = clean_ticker(stock)
        try:
            yf_ticker = yf.Ticker(ticker)
            hist_df = yf_ticker.history(period=period, interval=interval)
            if not hist_df.empty:
                closes[ticker] = hist_df['Close']
        except Exception:
            continue
    if not closes:
        return pd.DataFrame()
    combined = pd.DataFrame(closes)
    combined.index.name = 'Date'
    return combined.reset_index()
