"""
Test script for DDL to DML conversion functionality.

This script tests the new ddl_to_dml and generate_dml_from_ddl_folder functions.
"""

from pg_data_generator.main import generate_dml_from_ddl_folder, ddl_to_dml
import os
import shutil


def test_ddl_folder_to_dml():
    """Test converting a folder of DDL files to DML INSERT statements."""
    print("=" * 70)
    print("TEST 1: Converting DDL folder to DML INSERT statements")
    print("=" * 70)

    ddl_folder = './example_ddl'
    output_dml_dir = './test_output_dml'

    # Clean up output directory if it exists
    if os.path.exists(output_dml_dir):
        shutil.rmtree(output_dml_dir)

    try:
        # Test with keep_temp_files=True to see intermediate files
        result = generate_dml_from_ddl_folder(
            ddl_folder_path=ddl_folder,
            output_dml_dir=output_dml_dir,
            row_count=20,
            batch_size=10,
            keep_temp_files=True
        )

        print("\n" + "=" * 70)
        print("RESULTS:")
        print("=" * 70)
        print(f"✓ Tables generated: {result['tables']}")
        print(f"✓ DML files created: {len(result['dml_files'])}")
        print(f"✓ Schema saved at: {result.get('schema_path', 'N/A')}")
        print(f"✓ Data directory: {result.get('data_dir', 'N/A')}")

        print("\n" + "=" * 70)
        print("GENERATED DML FILES:")
        print("=" * 70)
        for dml_file in result['dml_files']:
            print(f"  - {dml_file}")
            # Show first few lines of each DML file
            with open(dml_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]
                print(f"    Preview (first 10 lines):")
                for line in lines:
                    print(f"    {line.rstrip()}")
                print()

        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_single_ddl_to_dml():
    """Test converting a single DDL file to DML."""
    print("\n" + "=" * 70)
    print("TEST 2: Converting single DDL file to DML")
    print("=" * 70)

    ddl_file = './example_ddl/example.sql'
    output_dml_dir = './test_output_dml_single'

    # Clean up output directory if it exists
    if os.path.exists(output_dml_dir):
        shutil.rmtree(output_dml_dir)

    try:
        result = ddl_to_dml(
            ddl_file_path=ddl_file,
            output_dml_dir=output_dml_dir,
            row_count=15,
            batch_size=5,
            keep_temp_files=False
        )

        print("\n" + "=" * 70)
        print("RESULTS:")
        print("=" * 70)
        print(f"✓ Tables generated: {result['tables']}")
        print(f"✓ DML files created: {len(result['dml_files'])}")

        print("\n" + "=" * 70)
        print("GENERATED DML FILES:")
        print("=" * 70)
        for dml_file in result['dml_files']:
            print(f"  - {dml_file}")

        return True

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("\n🚀 Starting DDL to DML Conversion Tests\n")

    test1_passed = test_ddl_folder_to_dml()
    test2_passed = test_single_ddl_to_dml()

    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Test 1 (DDL folder to DML): {'✓ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Test 2 (Single DDL to DML): {'✓ PASSED' if test2_passed else '❌ FAILED'}")

    if test1_passed and test2_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
