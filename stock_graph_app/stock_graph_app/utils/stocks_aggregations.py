import pandas as pd

def group_by_stock(df: pd.DataFrame) -> pd.DataFrame:
    """
    Groups the DataFrame by the 'Stock' column and aggregates the 'Cantidad_Comprada' column as a numeric sum.

    Args:
        df (pd.DataFrame): The filtered DataFrame with at least 'Stock' and 'Cantidad_Comprada' columns.

    Returns:
        pd.DataFrame: Grouped DataFrame with each stock and total 'Cantidad_Comprada'.
    """
    # Ensure Cantidad_Comprada is numeric (handle various European/US formats)
    import re
    def clean_quantity(val):
        s = str(val)
        # Remove all dots except the last one (for thousands separator)
        if s.count('.') > 1:
            parts = s.split('.')
            s = ''.join(parts[:-1]) + '.' + parts[-1]
        # Replace commas with dots (for decimal separator)
        s = s.replace(',', '.')
        try:
            return float(s)
        except Exception:
            return 0.0
    df = df.copy()
    df['Cantidad_Comprada'] = df['Cantidad_Comprada'].apply(clean_quantity)
    grouped = df.groupby('Stock', as_index=False)['Cantidad_Comprada'].sum()
    grouped = grouped.rename(columns={'Cantidad_Comprada': 'Total_Comprada'})
    return grouped
