# your_app_name/utils.py

#from os import os
#from dotenv import load_dotenv
import pandas as pd
import reflex as rx # Import reflex for rx.toast if you want to use it here for debugging/server-side messages

# Auto-load environment variables from .env
#load_dotenv()

#FORM_BRICKS_SHEET_URL="https://docs.google.com/spreadsheets/d/aaaaaaaa/export?format=csv"
# IMPORTANT: Set the Google Sheet URL as an environment variable named FORM_BRICKS_SHEET_URL


def fetch_gsheet_as_dataframe(gsheet_url: str) -> pd.DataFrame:
    """
    Fetches the contents of a Google Sheet (published as CSV) and returns it as a pandas DataFrame.

    Args:
        gsheet_url (str): The URL to the Google Sheet exported as CSV.
            Example: 'https://docs.google.com/spreadsheets/d/xxxx/export?format=csv&gid=yyyy'

    Returns:
        pd.DataFrame: The sheet data as a DataFrame. If loading fails, returns a DataFrame with an error message.
    """
    try:
        df = pd.read_csv(gsheet_url)
    except Exception as e:
        df = pd.DataFrame({"Error": [f"Failed to load CSV: {e}"]})
    return df


def filter_dataframe_columns(df: pd.DataFrame, columns: list[str], n_rows: int = None) -> pd.DataFrame:
    """
    Filters the given DataFrame to only the specified columns and optionally limits the number of rows.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        columns (list[str]): List of column names to keep. Columns not present are ignored.
        n_rows (int, optional): If provided, limits the DataFrame to the first n_rows rows.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    # Only keep columns that exist in df
    valid_columns = [col for col in columns if col in df.columns]
    filtered_df = df[valid_columns]
    if n_rows is not None:
        filtered_df = filtered_df.head(n_rows)
    return filtered_df