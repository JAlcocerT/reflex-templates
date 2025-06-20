# your_app_name/utils.py

import pandas as pd
import reflex as rx # Import reflex for rx.toast if you want to use it here for debugging/server-side messages

# IMPORTANT: Replace with your actual Google Sheet URL (CSV export)
# Make sure this URL is publicly accessible or your Reflex backend has access
FORM_BRICKS_SHEET_URL = "YOUR_GOOGLE_SHEET_CSV_EXPORT_URL_HERE" # <--- **UPDATE THIS**

# Function to check if an email is in FormBricks responses (Google Sheet)
def check_formbricks_subscription(email: str) -> bool:
    # In a real Reflex app, you wouldn't use st.error directly,
    # as streamlit is for a different type of app.
    # Instead, you'd handle exceptions and return a boolean or status.

    try:
        # Fetch the data from Google Sheets URL (assuming it's a CSV export URL)
        # Using a fixed URL for demonstration. In production, consider
        # more robust ways to handle external data sources (e.g., caching, background tasks)
        data = pd.read_csv(FORM_BRICKS_SHEET_URL)

        # If 'Extracted Email' column doesn't exist, derive it
        if 'Extracted Email' not in data.columns:
            # This assumes 'What is your contact information?' is always present
            # and contains the email at the end, as per your original script.
            if 'What is your contact information?' in data.columns:
                data['Extracted Email'] = data['What is your contact information?'].apply(lambda x: x.split(',')[-1].strip())
            else:
                rx.log("Warning: 'What is your contact information?' column not found for email extraction.")
                return False # Cannot validate without the correct column

        # Check if the email exists in the data
        is_subscribed = any(data['Extracted Email'].astype(str).str.lower() == email.lower())
        rx.log(f"Validation for email '{email}': {is_subscribed}") # For server-side logging
        return is_subscribed

    except Exception as e:
        rx.log(f"Error fetching FormBricks data for validation: {e}")
        # In a real app, you might want to log this error and inform the user
        return False