import os
import requests
import zipfile
import shutil

URL = "https://cricsheet.org/downloads/ipl.zip"
DOWNLOAD_PATH = "data/ipl.zip"
EXTRACT_DIR = "data/raw"

def fetch_and_extract():
    print("\U0001F4E5 Downloading IPL dataset from Cricsheet...")
    os.makedirs("data", exist_ok=True)
    response = requests.get(URL)
    with open(DOWNLOAD_PATH, "wb") as f:
        f.write(response.content)

    print("\U0001F4E6 Extracting ZIP...")
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    print(f"✅ Extracted {len(os.listdir(EXTRACT_DIR))} matches to {EXTRACT_DIR}")

if __name__ == "__main__":
    fetch_and_extract()
