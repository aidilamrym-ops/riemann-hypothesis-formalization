import os
import requests
import json

ZENODO_TOKEN = "r7Up4jMYMiaHtzCwKYRouhg2Hlm9Oa0QBUILmuGBdRrVA9wUwvqH6eNSvkSY"
ZENODO_URL = "https://zenodo.org/api/deposit/depositions"

headers = {"Authorization": f"Bearer {ZENODO_TOKEN}", "Content-Type": "application/json"}

print("Testing Zenodo API Connection...")
response = requests.get(ZENODO_URL, headers=headers)
print("Status Code:", response.status_code)
if response.status_code == 200:
    print("Zenodo Token Valid! Existing depositions found:", len(response.json()))
else:
    print("Response:", response.text)
