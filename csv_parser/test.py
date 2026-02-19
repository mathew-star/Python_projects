# generate_large_csv.py
import csv
import random
import string
from datetime import datetime, timedelta
import sys

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_date():
    start = datetime(2020, 1, 1)
    end = datetime(2024, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')

def generate_csv(filename, target_gb=5, flush_every=10000):
    """
    Generate CSV with realistic customer data.
    Target size in GB, actual size may vary slightly.
    """
    target_bytes = target_gb * 1024 * 1024 * 1024
    
    headers = [
        'Index', 'Customer Id', 'First Name', 'Last Name', 'Company',
        'City', 'Country', 'Phone 1', 'Phone 2', 'Email',
        'Subscription Date', 'Website'
    ]
    
    # Sample data pools
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 
                   'Michael', 'Linda', 'William', 'Elizabeth', 'David', 'Barbara',
                   'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah',
                   'Charles', 'Karen', 'Daniel', 'Nancy', 'Matthew', 'Lisa']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia',
                  'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez',
                  'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore']
    companies = ['TechCorp', 'GlobalInd', 'MegaSoft', 'DataSystems', 'CloudNine',
                 'ByteWorks', 'NetSolutions', 'DigitalDynamics', 'CyberSystems']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
              'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
              'London', 'Paris', 'Berlin', 'Tokyo', 'Sydney', 'Toronto']
    countries = ['United States', 'United Kingdom', 'Canada', 'Germany', 
                 'France', 'Japan', 'Australia', 'Netherlands', 'Singapore']
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
               'company.com', 'enterprise.org', 'business.net']
    
    written = 0
    row_count = 0
    file_size = 0
    
    print(f"Generating {target_gb}GB CSV: {filename}")
    print(f"Target: {target_bytes:,} bytes")
    
    with open(filename, 'w', newline='', buffering=8192) as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        while file_size < target_bytes:
            row = [
                row_count + 1,  # Index
                f"CUST-{random_string(8).upper()}",  # Customer Id
                random.choice(first_names),  # First Name
                random.choice(last_names),  # Last Name
                f"{random.choice(companies)} {random_string(5)}",  # Company
                random.choice(cities),  # City
                random.choice(countries),  # Country
                f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",  # Phone 1
                f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",  # Phone 2
                f"{random_string(8)}@{random.choice(domains)}",  # Email
                random_date(),  # Subscription Date
                f"https://www.{random_string(10)}.com"  # Website
            ]
            
            writer.writerow(row)
            row_count += 1
            
            # Progress update
            if row_count % flush_every == 0:
                f.flush()
                file_size = f.tell()
                progress = (file_size / target_bytes) * 100
                print(f"  Rows: {row_count:,} | Size: {file_size/1024/1024:.1f}MB | {progress:.1f}%", end='\r')
    
    print(f"\nDone! Generated {row_count:,} rows, {file_size/1024/1024/1024:.2f}GB")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--gb', type=float, default=5, help='Target size in GB')
    parser.add_argument('--out', default='customers_5gb.csv', help='Output filename')
    args = parser.parse_args()
    
    generate_csv(args.out, args.gb)