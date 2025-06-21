from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from udf_gsheet import fetch_gsheet_as_dataframe
from stocks_aggregations import group_by_stock
from stocks_combination_for_display import fetch_all_stocks_close_by_date, to_long_format_for_area_plot
from cagr import calculate_cagr


def main():
    # Load .env variables
    load_dotenv()
    gsheet_url = os.getenv("GOOGLE_SHEET_CSV_URL")
    if not gsheet_url:
        print("GOOGLE_SHEET_CSV_URL not found in .env!")
        return
    print(f"Using Google Sheet: {gsheet_url}")

    # Step 1: Fetch stock data from Google Sheets
    df = fetch_gsheet_as_dataframe(gsheet_url)
    print("\n[Step 1] Raw Data from Google Sheet:")
    print(df.head())

    # Step 2: Aggregate stocks
    agg_df = group_by_stock(df)
    print("\n[Step 2] Aggregated Stock List:")
    print(agg_df)

    # Step 3: Fetch historical close prices for these stocks
    stock_list = agg_df["Stock"].tolist()
    hist_df = fetch_all_stocks_close_by_date(stock_list, period="1y", interval="1d")
    print("\n[Step 3] Historical Close Prices:")
    print(hist_df.head())

    # Step 4: Convert to long format for CAGR
    long_df = to_long_format_for_area_plot(hist_df)
    print("\n[Step 4] Long Format Data for CAGR:")
    print(long_df.head())

    # Step 5: Calculate CAGR
    cagr_df = calculate_cagr(long_df)
    cagr_df["CAGR (%)"] = (cagr_df["CAGR"] * 100).round(2)
    print("\n[Step 5] CAGR Table (%):")
    print(cagr_df[["Stock", "CAGR (%)"]])

if __name__ == "__main__":
    main()
