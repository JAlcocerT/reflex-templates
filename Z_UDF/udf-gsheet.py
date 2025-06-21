# your_app_name/utils.py

import os
from dotenv import load_dotenv
import pandas as pd
import reflex as rx # Import reflex for rx.toast if you want to use it here for debugging/server-side messages

# Auto-load environment variables from .env
load_dotenv()

#FORM_BRICKS_SHEET_URL="https://docs.google.com/spreadsheets/d/aaaaaaaa/export?format=csv"
# IMPORTANT: Set the Google Sheet URL as an environment variable named FORM_BRICKS_SHEET_URL

FORM_BRICKS_SHEET_URL = os.environ.get("FORM_BRICKS_SHEET_URL")
print(FORM_BRICKS_SHEET_URL)
if not FORM_BRICKS_SHEET_URL:
    print("FORM_BRICKS_SHEET_URL environment variable is not set! Email validation will fail.")
    #FORM_BRICKS_SHEET_URL = ""

def get_authorized_emails() -> list:
    """Fetch and return the list of authorized emails from the 'Mail' column in the Google Sheet."""
    try:
        data = pd.read_csv(FORM_BRICKS_SHEET_URL)
        if 'Mail' not in data.columns:
            print("Warning: 'Mail' column not found in the sheet.")
            return []
        emails = data['Mail'].dropna().unique().tolist()
        return emails
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []

# Function to check if an email is in FormBricks responses (Google Sheet)
def check_formbricks_subscription(email: str) -> bool:
    # In a real Reflex app, you wouldn't use st.error directly,
    # as streamlit is for a different type of app.
    # Instead, you'd handle exceptions and return a boolean or status.

    try:
        # Fetch the data from Google Sheets URL (assuming it's a CSV export URL)
        # Using a fixed URL for demonstration. In production, consider
        # more robust ways to handle external data sources (e.g., caching, background tasks)
        authorized_emails = get_authorized_emails()
        is_subscribed = email.lower() in [e.lower() for e in authorized_emails]
        print(f"Validation for email '{email}': {is_subscribed}") # For server-side logging
        return is_subscribed

    except Exception as e:
        print(f"Error fetching FormBricks data for validation: {e}")
        # In a real app, you might want to log this error and inform the user
        return False