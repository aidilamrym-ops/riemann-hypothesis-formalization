import requests
import json
import os

ZENODO_TOKEN = "r7Up4jMYMiaHtzCwKYRouhg2Hlm9Oa0QBUILmuGBdRrVA9wUwvqH6eNSvkSY"
ZENODO_URL = "https://zenodo.org/api/deposit/depositions"

# 1. Create Deposition
headers = {"Authorization": f"Bearer {ZENODO_TOKEN}", "Content-Type": "application/json"}
data = {
    "metadata": {
        "title": "Sovereign Deterministic Verification of Foundational Lemmas for the Millennium Problems (v0.2)",
        "upload_type": "preprint",
        "description": "Formal verification of foundational lemmas using Lean 4 and Z3 SMT.",
        "creators": [{"name": "Amry, Muhammad Aidil", "affiliation": "Omega Cyber Guard"}]
    }
}
resp = requests.post(ZENODO_URL, headers=headers, json=data)
dep_id = resp.json()['id']
print(f"Deposition created: {dep_id}")

# 2. Upload file
bucket_url = resp.json()['links']['bucket']
file_path = "PaperA_Millennium_Verification.tex"
with open(file_path, "rb") as fp:
    requests.put(f"{bucket_url}/{file_path}", data=fp, headers={"Authorization": f"Bearer {ZENODO_TOKEN}"})
print("File uploaded.")

# 3. Publish (Skipping for now to keep it as a draft)
print("Draft created. Access: https://zenodo.org/deposit/{dep_id}")
