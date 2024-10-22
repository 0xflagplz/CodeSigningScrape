import os
import requests
import zipfile
import logging
from virustotal_python import Virustotal

# Configure logging
log_file = 'certdisco.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='a'),
        logging.StreamHandler()
    ]
)

def get_top_files(api_key, query, limit):
    vt = Virustotal(API_KEY=api_key)
    response = vt.request(
        "intelligence/search",
        params={"query": query, "limit": limit},
        method="GET"
    )
    return response.json().get("data", [])

def download_file(api_key, file_id, sha256, output_dir):
    vt = Virustotal(API_KEY=api_key)
    response = vt.request(f"files/{file_id}/download_url", method="GET")
    download_url = response.json().get('data')
    if download_url:
        file_response = requests.get(download_url, headers={"x-apikey": api_key})
        if file_response.status_code == 200:
            file_path = os.path.join(output_dir, sha256)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(file_response.content)
            logging.info(f"Downloaded and saved {file_path}")
            return file_path
        else:
            logging.error(f"Failed to download file {file_id}")
    else:
        logging.error(f"No download URL found for file {file_id}")
    return None


def vt_download(api_key, quantity, output_dir):
    query = "content:{02 01 03 30}@4 NOT tag:msi AND NOT tag:peexe AND ls:75d+ AND NOT p:5+"
    results = get_top_files(api_key, query, quantity)

    for obj in results:
        sha256 = obj['attributes'].get('sha256', 'N/A')
        names = obj['attributes'].get('names', ['N/A'])
        for name in names:
            logging.info(f"Name: {name}\nSha256: {sha256}\n")
            if '.p12' in name or '.pfx' in name:
                logging.info(f"Downloading {name} with SHA256: {sha256}")
                file_path = download_file(api_key, obj['id'], sha256, output_dir)
