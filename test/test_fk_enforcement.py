"""
Test script for FK enforcement.

This demonstrates that FK relationships are now properly enforced.
"""

from pg_data_generator.main import generate_data_from_ddl_folder
import pandas as pd
import os


def test_fk_enforcement():
    """Test that FK values are properly selected from referenced tables."""
    print("=" * 60)
    print("FK ENFORCEMENT TEST")
    print("=" * 60)

    # Create output directory
    output_dir = './test_fk_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate data from example DDL (has FK: MST_CUSTOMER.internal_no -> MST_EXAMPLE.id)
    try:
        tables, schema_path = generate_data_from_ddl_folder(
            ddl_folder_path='./example_ddl',
            output_data_dir=output_dir,
            row_count=10
        )

        print(f"\n✅ Successfully generated {len(tables)} tables: {tables}")
        print(f"Schema: {schema_path}")

        # Verify FK enforcement
        print("\n" + "=" * 60)
        print("VERIFYING FK ENFORCEMENT")
        print("=" * 60)

        # Load both tables
        customer_csv = os.path.join(output_dir, 'MST_CUSTOMER.csv')
        example_csv = os.path.join(output_dir, 'MST_EXAMPLE.csv')

        df_customer = pd.read_csv(customer_csv)
        df_example = pd.read_csv(example_csv)

        print(f"\nMST_EXAMPLE (referenced table) IDs:")
        print(df_example['id'].tolist())

        print(f"\nMST_CUSTOMER (referencing table) internal_no (FK) values:")
        print(df_customer['internal_no'].tolist())

        # Check that all FK values exist in referenced table
        valid_ids = set(df_example['id'].astype(str))
        fk_values = set(df_customer['internal_no'].astype(str))

        if fk_values.issubset(valid_ids):
            print(f"\n✅ FK ENFORCEMENT WORKING!")
            print(f"   All {len(fk_values)} FK values are valid references")
            print(f"   FK values: {sorted(fk_values)}")
            print(f"   Valid IDs: {sorted(valid_ids)}")
        else:
            invalid = fk_values - valid_ids
            print(f"\n❌ FK ENFORCEMENT FAILED!")
            print(f"   Invalid FK values found: {invalid}")

        # Show sample data
        print("\n" + "=" * 60)
        print("SAMPLE DATA")
        print("=" * 60)

        print("\nMST_EXAMPLE (first 5 rows):")
        print(df_example.head())

        print("\nMST_CUSTOMER (first 5 rows):")
        print(df_customer.head())

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_fk_enforcement()