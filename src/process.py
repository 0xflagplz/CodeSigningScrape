import os
import subprocess
import re
import threading
from src.parse import *

# Flag to indicate if the john process should be stopped
stop_john = False

def create_certificates_hash_file(directory):
    hash_file = os.path.join(directory, "certificates.hash")
    
    # Remove existing hash file if it exists
    if os.path.exists(hash_file):
        os.remove(hash_file)
    
    # Get all files in the directory
    files = os.listdir(directory)
    
    with open(hash_file, 'a') as hf:
        for file in files:
            file_path = os.path.join(directory, file)
            try:
                subprocess.run(f'pfx2john "{file_path}"', shell=True, check=True, stdout=hf, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                print(f"Failed to process file {file_path}, skipping.")
    
    return hash_file

def run_john_on_hashes(hash_file):
    global stop_john
    john_command = f"john --wordlist=/usr/share/wordlists/rockyou.txt --format=pfx {hash_file}"
    
    # Run john in a separate process
    john_process = subprocess.Popen(john_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try:
        while john_process.poll() is None:
            if stop_john:
                john_process.terminate()
                break
        john_process.wait()
    except KeyboardInterrupt:
        stop_john = True
        john_process.terminate()
        john_process.wait()

def get_cracked_passwords(hash_file):
    john_show_command = f"john --show --format=pfx {hash_file}"
    result = subprocess.run(john_show_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    
    cracked_passwords = {}
    
    for line in result.stdout.splitlines():
        # Adjust regex pattern to match the output format of John the Ripper
        match = re.match(r"^([^:]+):(.*?):", line)
        if match:
            hash_value = match.group(1).strip()
            password = match.group(2).strip() if match.group(2).strip() else "NULL"
            cracked_passwords[hash_value] = password
    
    return cracked_passwords

def intake(directory):
    hash_file = create_certificates_hash_file(directory)
    if hash_file:
        john_thread = threading.Thread(target=run_john_on_hashes, args=(hash_file,))
        john_thread.start()
        print("[*] Hashes are running though rockyou\n[*] Cancelation will still upload discovered hashes.")
        try:
            while john_thread.is_alive():
                john_thread.join(timeout=1)
        except KeyboardInterrupt:
            print("Process interrupted. Attempting to cancel john process...")
            global stop_john
            stop_john = True
            john_thread.join()
        finally:
            cracked_passwords = get_cracked_passwords(hash_file)
            for hash_value, password in cracked_passwords.items():
                # Check if directory path ends with a slash, and append hash_value accordingly
                if not directory.endswith('/') and not directory.endswith('\\'):
                    directory += '/'
                path = directory + hash_value
                parsing101(path, password)


