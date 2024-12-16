# -*- coding: utf-8 -*-
"""Pull_And_Create_CSV

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rmVDmoJyPCdH4QT0JCk0zoTSpcj1DkFU
"""

import requests
import pandas as pd
import os
from datetime import datetime

# Define your API key here (replace 'YOUR_API_KEY' with your actual key)
BLS_API_KEY = "22fddc1846284403b42a8a2326b03d8f"

# Define the BLS series to pull
data_series = [
    {"series_id": "CES0000000001", "name": "Nonfarm Payrolls"},
    {"series_id": "LNS14000000", "name": "Unemployment Rate"},
    {"series_id": "LNS11000000", "name": "Civilian Labor Force"},
    {"series_id": "CES0500000003", "name": "Avg Hourly Earnings (Private)"}
]

# File path for the CSV file
file_path = "bls_data.csv"

# Function to pull data from the BLS API
def fetch_bls_data(series_id):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {"Content-Type": "application/json"}

    payload = {
        "seriesid": [series_id],
        "startyear": "2010",  # Adjust start year as needed
        "endyear": str(datetime.now().year),
        "registrationkey": BLS_API_KEY
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    if response.status_code == 200 and "Results" in response_data:
        return response_data["Results"]["series"][0]["data"]
    else:
        print(f"Error fetching data for series {series_id}: {response_data.get('message', 'Unknown error')}")
        return []

# Function to process and append data to the CSV file
def update_csv(data_series, file_path):
    all_data = []
    for series in data_series:
        bls_data = fetch_bls_data(series["series_id"])
        for entry in bls_data:
            all_data.append({
                "series_id": series["series_id"],
                "series_name": series["name"],
                "year": entry["year"],
                "period": entry["period"],
                "period_name": entry["periodName"],
                "value": entry["value"]
            })

    df_new = pd.DataFrame(all_data)

    if os.path.exists(file_path):
        # Load existing CSV
        df_existing = pd.read_csv(file_path)

        # Combine and drop duplicates
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.drop_duplicates(subset=["series_id", "year", "period"], inplace=True)
        df_combined.to_csv(file_path, index=False)
    else:
        # Create new CSV
        df_new.to_csv(file_path, index=False)

# Run the update
update_csv(data_series, file_path)

print(f"Data updated successfully in {file_path}")