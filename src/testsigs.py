import os
import sqlite3
import subprocess
import argparse
import shutil
import zipfile

def fetch_certificates_from_db(db_file="certificates.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''SELECT cert_hash, password FROM certificates''')
    certificates = cursor.fetchall()
    
    conn.close()
    return certificates

def run_limelighter(outputdir, certlocation, cert_hash, password):
    if password:
        cmd = [
            "limelighter",
            "-I", "src/example.exe",
            "-O", f"{outputdir}/{cert_hash}.exe",
            "-Real", f"{certlocation}/{cert_hash}",
            "-Password", password
        ]
    else:
        cmd = [
            "limelighter",
            "-I", "src/example.exe",
            "-O", f"{outputdir}/{cert_hash}.exe",
            "-Real", f"{certlocation}/{cert_hash}"
        ]
    
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_output_directory(outputdir):
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
        print(f"Created output directory: {outputdir}")
    else:
        print(f"Output directory already exists: {outputdir}")

def zip_directory(directory, zip_name):
    shutil.make_archive(zip_name, 'zip', directory)
    print(f"Zipped directory {directory} into {zip_name}.zip")

def remove_directory(directory):
    shutil.rmtree(directory)
    print(f"Removed directory {directory}")

def testsigs(certlocation, outputdir):
    create_output_directory(outputdir)
    
    certificates = fetch_certificates_from_db()
    
    for cert_hash, password in certificates:
        try:
            run_limelighter(outputdir, certlocation, cert_hash, password)
        except subprocess.CalledProcessError as e:
            print(f"Failed to run limelighter for cert_hash {cert_hash}: {e}")

    # Zip the output directory
    zip_name = outputdir
    zip_directory(outputdir, zip_name)
    
    # Remove the output directory
    remove_directory(outputdir)


