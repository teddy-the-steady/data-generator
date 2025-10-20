"""
Local test runner for pg-data-generator.

This script demonstrates how to use the pg-data-generator package locally.
It generates test data based on example.csv in the project root.
"""

from pg_data_generator.main import generate_data
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR.parent / "example.csv"


def run():
    """
    Run the data generator locally with example.csv.

    This will:
    1. Read the schema from ./example.csv
    2. Generate 10 rows of synthetic data per table
    3. Save output CSV files to the current directory
    """
    print("Starting data generation...")
    print("Schema file: ./example.csv")
    print("Output directory: current directory")
    print("Rows per table: 10")
    print("-" * 50)

    tables = generate_data(
        schema_csv_path=CSV_FILE,
        row_count=10,
        output_dir='.'
    )

    print(f"\nSuccessfully generated {len(tables)} table(s):")
    for table in tables:
        print(f"  - {table}.csv")
    print("\nData generation complete!")


if __name__ == '__main__':
    run()