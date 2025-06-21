import reflex as rx
import pandas as pd
import os

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # If python-dotenv not installed, skip

# Get Google Sheet CSV URL from environment variable
sheet_csv_url = os.environ.get(
    "GOOGLE_SHEET_CSV_URL",
    "https://docs.google.com/spreadsheets/d/abcdefghi/export?format=csv&gid=123456789"
)

# Load the data
try:
    df = pd.read_csv(sheet_csv_url)
except Exception as e:
    df = pd.DataFrame({"Error": [f"Failed to load CSV: {e}"]})

# Select a subset of columns for demonstration (customize as needed)
display_columns = df.columns[:3] if len(df.columns) >= 3 else df.columns

def google_sheet_data_table():
    return rx.data_table(
        data=df[list(display_columns)],
        pagination=True,
        search=True,
        sort=True,
        width="100%",
    )
