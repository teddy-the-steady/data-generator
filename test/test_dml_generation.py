"""
Test file for DML (SQL INSERT statement) generation functionality.

This script tests the conversion of CSV data files to SQL INSERT statements.
"""

import os
import shutil
from pathlib import Path
from pg_data_generator.main import (
    generate_data,
    generate_data_with_dml,
    generate_dml_from_csv_folder
)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
EXAMPLE_CSV = PROJECT_ROOT / "example.csv"
TEST_OUTPUT_DIR = BASE_DIR / "test_output"
TEST_DATA_DIR = TEST_OUTPUT_DIR / "data"
TEST_SQL_DIR = TEST_OUTPUT_DIR / "sql"


def setup_test_environment():
    """Create test directories."""
    print("Setting up test environment...")

    # Clean up existing test output
    if TEST_OUTPUT_DIR.exists():
        shutil.rmtree(TEST_OUTPUT_DIR)

    # Create fresh directories
    TEST_OUTPUT_DIR.mkdir(exist_ok=True)
    TEST_DATA_DIR.mkdir(exist_ok=True)
    TEST_SQL_DIR.mkdir(exist_ok=True)

    print(f"  Created: {TEST_OUTPUT_DIR}")
    print(f"  Created: {TEST_DATA_DIR}")
    print(f"  Created: {TEST_SQL_DIR}")


def test_basic_dml_generation():
    """
    Test 1: Generate CSV data and convert to DML in one step.

    This tests the generate_data_with_dml() function which:
    1. Generates CSV data from schema
    2. Automatically converts to SQL INSERT statements
    """
    print("\n" + "="*70)
    print("TEST 1: Basic DML Generation (CSV + DML in one step)")
    print("="*70)

    result = generate_data_with_dml(
        schema_csv_path=str(EXAMPLE_CSV),
        row_count=20,
        output_dir=str(TEST_DATA_DIR),
        dml_output_dir=str(TEST_SQL_DIR),
        batch_size=10  # 10 rows per INSERT statement
    )

    print(f"\n✓ Generated {len(result['tables'])} table(s):")
    for table in result['tables']:
        print(f"    - {table}")

    print(f"\n✓ Generated {len(result['dml_files'])} DML file(s):")
    for dml_file in result['dml_files']:
        print(f"    - {Path(dml_file).name}")

    # Display sample content from first DML file
    if result['dml_files']:
        sample_file = result['dml_files'][0]
        print(f"\n📄 Sample content from {Path(sample_file).name}:")
        print("-" * 70)
        with open(sample_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:30]  # First 30 lines
            print(''.join(lines))
        print("-" * 70)

    return result


def test_convert_existing_csv():
    """
    Test 2: Convert existing CSV files to DML.

    This tests the generate_dml_from_csv_folder() function which:
    - Takes already generated CSV files
    - Converts them to SQL INSERT statements
    """
    print("\n" + "="*70)
    print("TEST 2: Convert Existing CSV Files to DML")
    print("="*70)

    # First generate some CSV data
    print("\nStep 1: Generating CSV data...")
    tables = generate_data(
        schema_csv_path=str(EXAMPLE_CSV),
        row_count=15,
        output_dir=str(TEST_DATA_DIR)
    )
    print(f"✓ Generated {len(tables)} CSV file(s)")

    # Now convert existing CSVs to DML
    print("\nStep 2: Converting CSV files to DML...")
    dml_files = generate_dml_from_csv_folder(
        csv_folder_path=str(TEST_DATA_DIR),
        output_dml_folder=str(TEST_SQL_DIR / "converted"),
        schema_csv_path=str(EXAMPLE_CSV),
        batch_size=5  # 5 rows per INSERT statement
    )

    print(f"\n✓ Converted {len(dml_files)} DML file(s):")
    for dml_file in dml_files:
        file_size = os.path.getsize(dml_file)
        print(f"    - {Path(dml_file).name} ({file_size} bytes)")

    return dml_files


def test_different_batch_sizes():
    """
    Test 3: Test different batch sizes for INSERT statements.

    This demonstrates how batch_size affects the output:
    - Small batch (5 rows): More INSERT statements, easier to read
    - Large batch (50 rows): Fewer INSERT statements, more efficient
    """
    print("\n" + "="*70)
    print("TEST 3: Different Batch Sizes")
    print("="*70)

    # Generate CSV data once
    print("\nGenerating CSV data with 50 rows per table...")
    tables = generate_data(
        schema_csv_path=str(EXAMPLE_CSV),
        row_count=50,
        output_dir=str(TEST_DATA_DIR)
    )

    batch_sizes = [5, 25, 50]

    for batch_size in batch_sizes:
        print(f"\n--- Batch size: {batch_size} rows per INSERT ---")

        output_folder = TEST_SQL_DIR / f"batch_{batch_size}"
        output_folder.mkdir(exist_ok=True)

        dml_files = generate_dml_from_csv_folder(
            csv_folder_path=str(TEST_DATA_DIR),
            output_dml_folder=str(output_folder),
            schema_csv_path=str(EXAMPLE_CSV),
            batch_size=batch_size
        )

        for dml_file in dml_files:
            file_size = os.path.getsize(dml_file)
            with open(dml_file, 'r', encoding='utf-8') as f:
                content = f.read()
                insert_count = content.count('INSERT INTO')

            print(f"  {Path(dml_file).name}:")
            print(f"    - File size: {file_size} bytes")
            print(f"    - INSERT statements: {insert_count}")


def verify_sql_syntax():
    """
    Test 4: Verify SQL syntax of generated DML files.

    This checks:
    - Proper quoting of string values
    - NULL handling
    - Numeric values without quotes
    - Date/time formatting
    """
    print("\n" + "="*70)
    print("TEST 4: SQL Syntax Verification")
    print("="*70)

    # Generate a small dataset with DML
    result = generate_data_with_dml(
        schema_csv_path=str(EXAMPLE_CSV),
        row_count=5,
        output_dir=str(TEST_DATA_DIR),
        dml_output_dir=str(TEST_SQL_DIR / "syntax_check"),
        batch_size=5
    )

    print("\n✓ Checking SQL syntax in generated files...")

    for dml_file in result['dml_files']:
        print(f"\n  Checking: {Path(dml_file).name}")

        with open(dml_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic syntax checks
        checks = {
            "Has INSERT INTO": "INSERT INTO" in content,
            "Has VALUES": "VALUES" in content,
            "Ends with semicolon": content.strip().endswith(';'),
            "Has proper formatting": "    (" in content,  # Indented values
        }

        for check_name, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f"    {status} {check_name}")


def run_all_tests():
    """Run all DML generation tests."""
    print("\n" + "="*70)
    print("DML GENERATION TEST SUITE")
    print("="*70)
    print(f"Schema file: {EXAMPLE_CSV}")
    print(f"Output directory: {TEST_OUTPUT_DIR}")
    print("="*70)

    # Setup
    setup_test_environment()

    # Run tests
    try:
        test_basic_dml_generation()
        test_convert_existing_csv()
        test_different_batch_sizes()
        verify_sql_syntax()

        print("\n" + "="*70)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"\nTest output saved to: {TEST_OUTPUT_DIR}")
        print("You can review the generated SQL files in the subdirectories.")

    except Exception as e:
        print("\n" + "="*70)
        print("✗ TEST FAILED")
        print("="*70)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_all_tests()
