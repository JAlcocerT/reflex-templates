import pandas as pd
from typing import Union

def calculate_cagr(
    df: pd.DataFrame,
    stock_column: str = "Stock",
    date_column: str = "Date",
    value_column: str = "Close",
) -> pd.DataFrame:
    """
    Calculate the Compound Annual Growth Rate (CAGR) for each stock in the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame in long format with columns for stock, date, and value.
        stock_column (str): Column name for stock identifier.
        date_column (str): Column name for date.
        value_column (str): Column name for price/value.
    Returns:
        pd.DataFrame: DataFrame with columns [stock_column, 'CAGR']
    """
    cagr_list = []
    for stock, group in df.groupby(stock_column):
        group = group.sort_values(date_column)
        if group.shape[0] < 2:
            cagr = None
        else:
            initial = group.iloc[0][value_column]
            final = group.iloc[-1][value_column]
            # Calculate number of years between first and last date
            try:
                years = (pd.to_datetime(group.iloc[-1][date_column]) - pd.to_datetime(group.iloc[0][date_column])).days / 365.25
            except Exception:
                years = None
            if years and years > 0 and initial > 0 and final > 0:
                cagr = (final / initial) ** (1 / years) - 1
            else:
                cagr = None
        cagr_list.append({stock_column: stock, "CAGR": cagr})
    return pd.DataFrame(cagr_list)
