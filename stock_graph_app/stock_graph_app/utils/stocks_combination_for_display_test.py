import os
from dotenv import load_dotenv
from udf_gsheet import fetch_gsheet_as_dataframe, filter_dataframe_columns
from stocks_aggregations import group_by_stock
from stocks_combination_for_display import fetch_and_aggregate_stocks, fetch_all_stocks_close_by_date, to_long_format_for_area_plot

def test_stocks_combination_utils():
    load_dotenv()
    url = os.environ.get("GOOGLE_SHEET_CSV_URL")
    assert url, "GOOGLE_SHEET_CSV_URL must be set in .env for testing."
    df = fetch_gsheet_as_dataframe(url)
    filtered_df = filter_dataframe_columns(df, ["Stock", "Cantidad_Comprada"], n_rows=None)
    grouped_df = group_by_stock(filtered_df)
    stock_list = list(grouped_df["Stock"])
    print("\nTesting fetch_and_aggregate_stocks:")
    agg_df = fetch_and_aggregate_stocks(stock_list)
    print(agg_df)
    assert not agg_df.empty, "Aggregated stocks DataFrame should not be empty."
    print("\nTesting fetch_all_stocks_close_by_date:")
    close_table = fetch_all_stocks_close_by_date(stock_list)
    print(close_table.head())
    assert not close_table.empty, "Combined close table should not be empty."

    print("\nTesting to_long_format_for_area_plot:")
    long_df = to_long_format_for_area_plot(close_table)
    print(long_df.head())
    assert not long_df.empty, "Long format DataFrame should not be empty."
    assert set(long_df.columns) == {"Date", "Stock", "Close"}, "Long format columns incorrect."

if __name__ == "__main__":
    test_stocks_combination_utils()
    print("stocks_combination_for_display tests completed.")
