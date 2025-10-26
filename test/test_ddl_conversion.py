from pg_data_generator.main import ddl_folder_to_csv, generate_data_from_ddl_folder
import os


def test_ddl_folder_to_csv():
    print("=" * 60)
    print("TEST 1: Convert DDL folder to CSV")
    print("=" * 60)

    try:
        ddl_folder_to_csv(
            folder_path='./example_ddl',
            output_csv_path='./test_schema.csv'
        )
        print("\n✅ Test 1 PASSED: DDL converted to CSV successfully")
        print("   Output: test_schema.csv")

        print("\nGenerated CSV content:")
        print("-" * 60)
        with open('./test_schema.csv', 'r') as f:
            print(f.read())

    except Exception as e:
        print(f"\n❌ Test 1 FAILED: {e}")
        import traceback
        traceback.print_exc()


def test_generate_from_ddl():
    """Test generating data directly from DDL folder."""
    print("\n" + "=" * 60)
    print("TEST 2: Generate data from DDL folder")
    print("=" * 60)

    try:
        output_dir = './test_output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        tables, schema_path = generate_data_from_ddl_folder(
            ddl_folder_path='./example_ddl',
            output_data_dir=output_dir,
            row_count=5
        )

        print(f"\n✅ Test 2 PASSED: Generated {len(tables)} tables")
        print(f"   Tables: {tables}")
        print(f"   Schema: {schema_path}")
        print(f"   Output directory: {output_dir}")

        for table in tables:
            csv_file = os.path.join(output_dir, f"{table}.csv")
            if os.path.exists(csv_file):
                print(f"\n{table}.csv (first 3 rows):")
                print("-" * 60)
                with open(csv_file, 'r') as f:
                    lines = f.readlines()[:4]  # header + 3 rows
                    print(''.join(lines))

    except Exception as e:
        print(f"\n❌ Test 2 FAILED: {e}")
        import traceback
        traceback.print_exc()


def test_comments_and_references():
    """Test that comments are removed and REFERENCES syntax works."""
    print("\n" + "=" * 60)
    print("TEST 3: Verify comments and REFERENCES handling")
    print("=" * 60)

    try:
        from pg_data_generator.utils.ddl_converter import parse_ddl_string

        ddl = """
        -- Single line comment at the top
        CREATE TABLE test_table (
            id INT PRIMARY KEY,  -- inline comment
            fk_col INT REFERENCES other_table(id),  -- FK with REFERENCES
            name VARCHAR(50)
        );
        /* Multi-line comment
           should be ignored */
        """

        tables = parse_ddl_string(ddl)

        if len(tables) == 1:
            table = tables[0]
            print(f"\n✅ Test 3 PASSED: Parsed table: {table['table_name']}")
            print(f"   Columns: {len(table['columns'])}")

            for col in table['columns']:
                print(f"   - {col['name']}: {col['type']}", end="")
                if col.get('is_primary_key'):
                    print(" [PK]", end="")
                if col.get('foreign_key'):
                    fk_table, fk_col = col['foreign_key']
                    print(f" [FK -> {fk_table}.{fk_col}]", end="")
                print()

            # Verify FK was captured correctly
            fk_col = [c for c in table['columns'] if c['name'] == 'fk_col'][0]
            if fk_col.get('foreign_key') == ('other_table', 'id'):
                print("\n   ✅ REFERENCES syntax parsed correctly")
            else:
                print(f"\n   ❌ FK parsing failed: {fk_col.get('foreign_key')}")
        else:
            print(f"\n❌ Test 3 FAILED: Expected 1 table, got {len(tables)}")

    except Exception as e:
        print(f"\n❌ Test 3 FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    print("\nDDL Conversion Test Suite")
    print("=" * 60)

    test_ddl_folder_to_csv()
    test_generate_from_ddl()
    test_comments_and_references()

    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("=" * 60)
