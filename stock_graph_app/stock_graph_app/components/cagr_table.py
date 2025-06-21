import reflex as rx
from stock_graph_app.states.stock_state import StockState
from stock_graph_app.utils.cagr import calculate_cagr
import pandas as pd


def cagr_table() -> rx.Component:
    # Get the long-format data from state (assuming it's stored as a list of dicts)
    # You may need to adjust this if your state structure is different
    long_df = pd.DataFrame(getattr(StockState, "long_format_data", []))
    if long_df.empty or not set(["Stock", "Date", "Close"]).issubset(long_df.columns):
        return rx.el.div(
            "CAGR data not available.",
            class_name="text-neutral-400 italic text-center my-4",
        )
    cagr_df = calculate_cagr(long_df)
    cagr_df["CAGR (%)"] = (cagr_df["CAGR"] * 100).round(2)
    # Build table rows
    table_rows = [
        rx.table.row(
            rx.table.row_header_cell(str(row["Stock"])),
            rx.table.cell(f"{row['CAGR (%)']}%" if row["CAGR (%)"] is not None else "-"),
        )
        for _, row in cagr_df.iterrows()
    ]
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Stock"),
                rx.table.column_header_cell("CAGR (%)"),
            ),
        ),
        rx.table.body(*table_rows),
        width="100%",
        class_name="my-4",
    )
