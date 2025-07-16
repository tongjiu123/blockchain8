import pandas as pd
from faker import Faker
from tqdm import tqdm
import os
import hashlib
import random
from web3 import Web3

# --- Configuration ---
NUM_RECORDS = 100_000  # Full dataset size as specified in requirements
# Use an absolute path to ensure the file is saved in the correct location
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset'))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'certificates_data.csv')

# --- Main Function ---
def generate_dataset():
    """
    Generates a large, realistic dataset of academic certificates and saves it to a CSV file.
    The dataset includes a pre-computed keccak256 hash for each certificate record, which
    will be used for on-chain transactions in the simulation.
    """
    print(f"Starting dataset generation for {NUM_RECORDS} records...")

    fake = Faker()

    degree_types = [
        "Bachelor of Science",
        "Master of Engineering",
        "Doctor of Philosophy",
        "Bachelor of Arts",
        "Master of Business Administration"
    ]
    institutions = [
        "University of Tech", "Global Science Institute", "National Research University",
        "State College of Engineering", "Metropolis Business School"
    ]
    majors = ['Computer Science', 'Data Science', 'Electrical Engineering', 'Mechanical Engineering', 'Business Administration', 'Economics', 'Art History']

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = []
    for _ in tqdm(range(NUM_RECORDS), desc="Generating Records"):
        record = {
            'student_name': fake.name(),
            'degree_type': random.choice(degree_types),
            'institution_name': random.choice(institutions),
            'major': random.choice(majors),
            'gpa': round(random.uniform(3.0, 4.0), 2),
            'graduation_year': random.randint(2020, 2025),
            'issue_date': fake.date_between(start_date='-4y', end_date='today').isoformat()
        }

        record_string = f"{record['student_name']},{record['degree_type']},{record['institution_name']},{record['major']},{record['gpa']},{record['graduation_year']},{record['issue_date']}"
        record['certificate_hash'] = Web3.keccak(record_string.encode('utf-8')).hex()
        data.append(record)

    df = pd.DataFrame(data)
    print(f"\nSaving dataset to {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nDataset generation complete!")
    print(f"Total records: {len(df)}")
    print(f"File saved at: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == '__main__':
    generate_dataset()
