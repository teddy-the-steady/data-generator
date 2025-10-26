from pg_data_generator.main import generate_data
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR.parent / "example.csv"


def run():
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