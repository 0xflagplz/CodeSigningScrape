import os
import subprocess
import sqlite3
from OpenSSL import crypto
from datetime import datetime

def extract_certificate(pfx_file, password):
    # Extract the certificate from the PFX file
    if password:
        cmd = [
            "openssl", "pkcs12", "-in", pfx_file, "-nokeys", "-out", "certificate.pem",
            "-passin", f"pass:{password}"
        ]
    else:
        cmd = [
            "openssl", "pkcs12", "-in", pfx_file, "-nokeys", "-out", "certificate.pem",
            "-passin", "pass:"
        ]
    subprocess.run(cmd, check=True)

def parse_certificate(cert_file, hash_value):
    # Load the certificate
    with open(cert_file, 'rb') as f:
        cert_data = f.read()
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)

    # Extract required information
    cert_hash = hash_value
    issuer = cert.get_issuer().get_components()
    subject = cert.get_subject().get_components()
    cn = dict(subject).get(b'CN', b'').decode('utf-8')
    not_before = datetime.strptime(cert.get_notBefore().decode('utf-8'), '%Y%m%d%H%M%SZ')
    not_after = datetime.strptime(cert.get_notAfter().decode('utf-8'), '%Y%m%d%H%M%SZ')

    issuer_str = ', '.join([f"{key.decode('utf-8')}={value.decode('utf-8')}" for key, value in issuer])
    subject_str = ', '.join([f"{key.decode('utf-8')}={value.decode('utf-8')}" for key, value in subject])

    return cert_hash, issuer_str, subject_str, cn, not_before, not_after

def store_certificate_info(cert_info, password):
    db_file = "certificates.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS certificates (
                        id INTEGER PRIMARY KEY,
                        cert_hash TEXT UNIQUE,
                        issuer TEXT,
                        subject TEXT,
                        cn TEXT,
                        not_before TEXT,
                        not_after TEXT,
                        password TEXT
                      )''')

    # Check for existing certificate
    cursor.execute('''SELECT 1 FROM certificates WHERE cert_hash = ?''', (cert_info[0],))
    if cursor.fetchone() is not None:
        print("[+] Certificate already exists in the database.")
    else:
        # Insert certificate information
        cursor.execute('''INSERT INTO certificates (cert_hash, issuer, subject, cn, not_before, not_after, password)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', (*cert_info, password or None))
        print("[+] New certificate information stored in the database.")
    
    conn.commit()
    conn.close()

def cleanup_files():
    if os.path.exists("certificate.pem"):
        os.remove("certificate.pem")

def parsing101(pfx_file, password, hash_value):

    if not os.path.exists(pfx_file):
        print(f"File {pfx_file} does not exist.")
        return  # Exit early if the file does not exist

    if password == "NULL":
        password = ""

    try:
        extract_certificate(pfx_file, password)
        cert_info = parse_certificate("certificate.pem", hash_value)
        store_certificate_info(cert_info, password)
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract certificate: {e}")
    except crypto.Error as e:
        print(f"Failed to parse certificate: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        cleanup_files()