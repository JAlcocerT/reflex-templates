# https://github.com/JAlcocerT/Streamlit-AIssistant/blob/main/Z_Auth_Ways/Auth_FormBricks.py

# Auth_FormBricks.py

import pandas as pd
import streamlit as st

# Function to check if an email is in FormBricks responses (Google Sheet)
def check_formbricks_subscription(email, sheet_url, auth_mode):
    if "FormBricks" not in auth_mode:
        return False  # Skip if FormBricks is not in AUTH_MODE
    
    try:
        # Fetch the data from Google Sheets URL (assuming it's a CSV export URL)
        data = pd.read_csv(sheet_url)
        
        # If 'Extracted Email' column doesn't exist, derive it
        if 'Extracted Email' not in data.columns:
            data['Extracted Email'] = data['What is your contact information?'].apply(lambda x: x.split(',')[-1].strip())
        
        # Check if the email exists in the data
        return any(data['Extracted Email'] == email)
    
    except Exception as e:
        st.error(f"Error fetching FormBricks data: {e}")
        return False