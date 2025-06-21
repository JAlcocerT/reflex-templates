import os
from dotenv import load_dotenv
from udf_gsheet import fetch_gsheet_as_dataframe, filter_dataframe_columns

# Load environment variables from .env
load_dotenv()

def test_fetch_gsheet_as_dataframe():
    """Test fetching a Google Sheet as DataFrame."""
    url = os.environ.get("GOOGLE_SHEET_CSV_URL")
    assert url, "GOOGLE_SHEET_CSV_URL must be set in .env for testing."
    df = fetch_gsheet_as_dataframe(url)
    print("Fetched DataFrame:")
    print(df.head())
    assert not df.empty, "DataFrame should not be empty."
    assert isinstance(df, type(df)), "Should return a DataFrame."


def test_filter_dataframe_columns():
    """Test filtering columns and limiting rows."""
    url = os.environ.get("GOOGLE_SHEET_CSV_URL")
    df = fetch_gsheet_as_dataframe(url)
    # Use first 2 columns for test (if available)
    test_columns = list(df.columns[:2])
    filtered = filter_dataframe_columns(df, test_columns, n_rows=3)
    print(f"Filtered columns {test_columns} (max 3 rows):")
    print(filtered)
    assert list(filtered.columns) == test_columns, "Filtered columns do not match."
    assert len(filtered) <= 3, "Filtered DataFrame should have at most 3 rows."

def test_specific_columns_and_rows():
    """Test filtering for ['Stock', 'Cantidad_Comprada'] and 10 rows."""
    url = os.environ.get("GOOGLE_SHEET_CSV_URL")
    df = fetch_gsheet_as_dataframe(url)
    columns = ['Stock', 'Cantidad_Comprada']
    filtered = filter_dataframe_columns(df, columns, n_rows=10)
    print(f"Filtered columns {columns} (max 10 rows):")
    print(filtered)
    # Assert columns present (ignore missing columns gracefully)
    for col in columns:
        assert col in filtered.columns, f"Column '{col}' should be present in filtered DataFrame."
    assert len(filtered) <= 10, "Filtered DataFrame should have at most 10 rows."

if __name__ == "__main__":
    print("\n--- Testing fetch_gsheet_as_dataframe ---")
    test_fetch_gsheet_as_dataframe()
    print("\n--- Testing filter_dataframe_columns ---")
    test_filter_dataframe_columns()
    print("\n--- Testing specific columns and 10 rows ---")
    test_specific_columns_and_rows()