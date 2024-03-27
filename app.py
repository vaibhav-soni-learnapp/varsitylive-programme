import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import date

# Streamlit application title
st.title('API Clicks Fetcher')

# Authorization token (hardcoded for demonstration; consider securely managing this)
auth_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIxODUyZmZmNi02N2RlLTRiNjYtYmIwMy01NDJlY2Q4YmZmNzMiLCJhZG0iOnRydWUsImlhdCI6MTcxMTUzOTg3NCwiZXhwIjoxNzExNjI2Mjc0LCJhdWQiOiJwbGF0bzowLjAuMSIsImlzcyI6InZhcnNpdHktbGl2ZSJ9.kLD0426faR5bf8QPJsEgahIbBF8s5n0Tf83V4WhUbFA'  # Ensure to replace <your_token_here> with your actual tokeneyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIxODUyZmZmNi02N2RlLTRiNjYtYmIwMy01NDJlY2Q4YmZmNzMiLCJhZG0iOnRydWUsImlhdCI6MTcxMTUzOTg3NCwiZXhwIjoxNzExNjI2Mjc0LCJhdWQiOiJwbGF0bzowLjAuMSIsImlzcyI6InZhcnNpdHktbGl2ZSJ9.kLD0426faR5bf8QPJsEgahIbBF8s5n0Tf83V4WhUbFA
headers = {'Authorization': auth_token}

# Function to fetch clicks data
def fetch_clicks(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.content:
        return response.json()
    else:
        return f"Error fetching data: {response.status_code}"

# Fetch event names for dropdown
all_clicks_url = "https://oracle.varsitylive.in/admin/web-analytics/click/all"
all_clicks_response = fetch_clicks(all_clicks_url)
if isinstance(all_clicks_response, str):
    st.error(all_clicks_response)
else:
    event_names = [event['eventName'] for event in all_clicks_response['items']]
    selected_event_name = st.selectbox('Select Event Name', event_names)

    # Date input for fromDate and toDate
    fromDate = st.date_input("From Date", date.today())
    toDate = st.date_input("To Date", date.today())

    # Dynamic URLs for the APIs based on selected event name and date range
    urls = [
        f"https://oracle.varsitylive.in/admin/web-analytics/click/{selected_event_name}/3f2973a2-b6f2-4c18-ba1d-4c48346937b6/range?fromDate={fromDate}&toDate={toDate}",
        f"https://oracle.varsitylive.in/admin/web-analytics/click/{selected_event_name}/f4747acb-e1f7-458a-94bb-1a154d256795/range?fromDate={fromDate}&toDate={toDate}"
    ]

    # Fetch and display data concurrently for the selected event name and date range
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_clicks, urls))

    # Display results
    for result in results:
        if isinstance(result, str):
            st.error(result)
        else:
            st.json(result)  # Use st.json for better formatting of JSON response

