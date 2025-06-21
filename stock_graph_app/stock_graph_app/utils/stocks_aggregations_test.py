import pandas as pd
from stock_graph_app.utils.udf_gsheet import fetch_gsheet_as_dataframe

def check_data_structure():
    """Check the structure of the actual data being used in the app."""
    print("Checking data structure...")
    
    # Find where the data is being loaded in the app
    # Let's look for where fetch_gsheet_as_dataframe is called
    try:
        # Try to find the Google Sheet URL in the code
        import os
        from pathlib import Path
        
        # Look for the URL in environment variables
        gsheet_url = os.environ.get('GSHEET_URL')
        if gsheet_url:
            print(f"Found GSHEET_URL in environment variables")
        else:
            # Look for the URL in the code
            import re
            app_dir = Path(__file__).parent / "stock_graph_app"
            for py_file in app_dir.rglob("*.py"):
                try:
                    content = py_file.read_text()
                    if 'fetch_gsheet_as_dataframe' in content:
                        print(f"Found fetch_gsheet_as_dataframe in {py_file}")
                        # Look for URL pattern in the file
                        urls = re.findall(r'https?://[^\s")]+', content)
                        for url in urls:
                            if 'docs.google.com' in url and 'export?format=csv' in url:
                                gsheet_url = url
                                print(f"Found Google Sheet URL: {url}")
                                break
                except Exception as e:
                    print(f"Error reading {py_file}: {e}")
        
        if not gsheet_url:
            print("Could not find Google Sheet URL. Please check your code where fetch_gsheet_as_dataframe is called.")
            return
        
        # Try to load the data
        print(f"\nLoading data from: {gsheet_url}")
        df = fetch_gsheet_as_dataframe(gsheet_url)
        
        # Print data structure
        print("\n=== Data Structure ===")
        print(f"Shape: {df.shape}")
        print("\nColumns:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i}. {col} (dtype: {df[col].dtype})")
        
        print("\nFirst 5 rows:")
        print(df.head().to_string())
        
        # Check for potential quantity columns
        print("\nPotential quantity columns (case insensitive search):")
        quantity_indicators = ['cantidad', 'qty', 'quantity', 'comprada', 'comprado']
        potential_qty_cols = [
            col for col in df.columns 
            if any(ind in str(col).lower() for ind in quantity_indicators)
        ]
        
        if potential_qty_cols:
            print("\nPotential quantity columns found:")
            for col in potential_qty_cols:
                print(f"- {col}")
                print(f"  Sample values: {df[col].head().tolist()}")
        else:
            print("No potential quantity columns found. Please check your data.")
        
    except Exception as e:
        print(f"Error checking data structure: {e}")

if __name__ == "__main__":
    check_data_structure()
