#https://github.com/JAlcocerT/Streamlit-AIssistant/blob/main/Z_Auth_Ways/Auth_Mailerlite.py

import requests
import streamlit as st

# Function to check if an email is in MailerLite subscribers
def check_mailerlite_subscription(email, api_key, base_url, auth_mode):
    if "MailerLite" not in auth_mode:
        return False  # Skip if MailerLite is not in AUTH_MODE
    
    # Define the endpoint
    endpoint = f'{base_url}/subscribers'
    
    # Set up headers with the MailerLite API key
    headers = {
        'Content-Type': 'application/json',
        'X-MailerLite-ApiKey': api_key
    }
    
    # Make the GET request to the MailerLite API
    response = requests.get(endpoint, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        subscribers = response.json()
        # Check if the email is in the list of subscribers
        return any(subscriber.get('email') == email for subscriber in subscribers)
    else:
        st.error(f"Error fetching subscribers from MailerLite: {response.status_code} - {response.text}")
        return False