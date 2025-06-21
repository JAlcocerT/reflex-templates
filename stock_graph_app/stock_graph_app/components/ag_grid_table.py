import reflex as rx
import pandas as pd
import os
import plotly.express as px

# Import the utility functions for Google Sheet loading and filtering
from stock_graph_app.utils.udf_gsheet import fetch_gsheet_as_dataframe, filter_dataframe_columns

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

# Load the data using the robust UDF
main_df = fetch_gsheet_as_dataframe(sheet_csv_url)

# Select a subset of columns for demonstration (customize as needed)
display_columns = main_df.columns[:3] if len(main_df.columns) >= 3 else main_df.columns

def google_sheet_data_table():
    return rx.data_table(
        data=main_df[list(display_columns)],
        pagination=True,
        search=True,
        sort=True,
        width="100%",
    )


def filtered_gsheet_data_table():
    """
    Shows the filtered Google Sheet data with only ['Stock', 'Cantidad_Comprada'] columns and all available rows.
    """
    filtered_df = filter_dataframe_columns(main_df, ["Stock", "Cantidad_Comprada"], n_rows=None)
    return rx.data_table(
        data=filtered_df,
        pagination=True,
        search=True,
        sort=True,
        width="100%",
    )

# --- Grouped Stock Table ---
from stock_graph_app.utils.stocks_aggregations import group_by_stock

def grouped_stock_table():
    """
    Shows the grouped data by 'Stock' with total 'Cantidad_Comprada'.
    """
    filtered_df = filter_dataframe_columns(main_df, ["Stock", "Cantidad_Comprada"], n_rows=None)
    grouped_df = group_by_stock(filtered_df)
    return rx.data_table(
        data=grouped_df,
        pagination=True,
        search=True,
        sort=True,
        width="100%",
    )


def stock_treemap():
    """
    Plotly treemap showing the distribution of Total_Comprada per Stock.
    """
    filtered_df = filter_dataframe_columns(main_df, ["Stock", "Cantidad_Comprada"], n_rows=None)
    grouped_df = group_by_stock(filtered_df)
    if grouped_df.empty or grouped_df["Total_Comprada"].sum() == 0:
        return rx.text("No data available for treemap.")
    fig = px.treemap(
        grouped_df,
        path=["Stock"],
        values="Total_Comprada",
        title="Distribution of Total Cantidad_Comprada per Stock",
    )
    return rx.center(rx.plotly(data=fig))
