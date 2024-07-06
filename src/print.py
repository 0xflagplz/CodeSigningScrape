import sqlite3
import csv
import argparse

def print_certificate_database():
    db_file = "certificates.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query to select all records from the certificates table
    cursor.execute("SELECT * FROM certificates")

    # Fetch all rows from the query result
    rows = cursor.fetchall()

    # Print the column headers
    print(f"{'ID':<5} {'Cert Hash':<64} {'Issuer':<50} {'Subject':<50} {'CN':<30} {'Not Before':<20} {'Not After':<20} {'Password':<15}")
    print("-" * 254)

    # Print each row
    for row in rows:
        id, cert_hash, issuer, subject, cn, not_before, not_after, password = row
        print(f"{id:<5} {cert_hash:<64} {issuer:<50} {subject:<50} {cn:<30} {not_before:<20} {not_after:<20} {password or '':<15}")

    conn.close()

def export_certificate_database_to_csv(csv_file):
    db_file = "certificates.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query to select all records from the certificates table
    cursor.execute("SELECT * FROM certificates")

    # Fetch all rows from the query result
    rows = cursor.fetchall()

    # Get column names from the cursor description
    column_names = [description[0] for description in cursor.description]

    # Write to CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)  # Write the column headers
        writer.writerows(rows)         # Write the data rows

    print(f"Database exported to {csv_file}")

    conn.close()
