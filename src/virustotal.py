import os
import requests
import zipfile
from virustotal_python import Virustotal

def get_top_files(api_key, query, limit):
    vt = Virustotal(API_KEY=api_key)
    response = vt.request(
        "intelligence/search",
        params={"query": query, "limit": limit},
        method="GET"
    )
    return response.json().get("data", [])

def download_file(api_key, file_id, file_name, output_dir):
    vt = Virustotal(API_KEY=api_key)
    response = vt.request(f"files/{file_id}/download_url", method="GET")
    download_url = response.json().get('data')
    if download_url:
        file_response = requests.get(download_url, headers={"x-apikey": api_key})
        if file_response.status_code == 200:
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, "wb") as f:
                f.write(file_response.content)
            print(f"Downloaded and saved {file_name}")
            return file_path
        else:
            print(f"Failed to download file {file_id}")
    else:
        print(f"No download URL found for file {file_id}")
    return None

def unzip_file_if_needed(file_path, extract_to, password="infected"):
    if zipfile.is_zipfile(file_path):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(path=extract_to, pwd=password.encode())
        os.remove(file_path)
        print(f"Extracted and removed {file_path}")
    else:
        print(f"The file {file_path} is not a valid zip file or does not need extraction.")

def vt_download(api_key, quantity, output_dir):
    query = "content:{02 01 03 30}@4 NOT tag:msi AND NOT tag:peexe AND ls:30d+"
    results = get_top_files(api_key, query, quantity)

    for obj in results:
        sha256 = obj['attributes'].get('sha256', 'N/A')
        names = obj['attributes'].get('names', ['N/A'])
        for name in names:
            print(f"Name: {name}\nSha256: {sha256}\n")
            if '.p12' in name or '.pfx' in name:
                print(f"Downloading {name} with SHA256: {sha256}")
                file_path = download_file(api_key, obj['id'], name, output_dir)
                if file_path:
                    unzip_file_if_needed(file_path, output_dir)
