"""
Main API module for pg-data-generator.

This module provides the public API for generating synthetic PostgreSQL data
from CSV schema definitions. Use this when importing the package from other repositories.
"""

from pg_data_generator.core.Csv import Csv
from pg_data_generator.core.DataGenerator import DataGenerator
from pg_data_generator.utils.ddl_converter import (
    ddl_to_csv,
    ddl_folder_to_csv,
    ddl_string_to_csv
)
from pg_data_generator.utils.dml_converter import (
    csv_to_dml,
    csv_folder_to_dml
)


def generate_data(schema_csv_path, row_count=10, output_dir=None):
    """
    Generate synthetic data based on a CSV schema file.

    Args:
        schema_csv_path (str): Path to the CSV schema file defining table structures
        row_count (int): Number of rows to generate for each table (default: 10)
        output_dir (str): Directory where output CSV files will be saved.
                         If None, files are saved in the current directory (default: None)

    Returns:
        list: List of generated table names

    Raises:
        Exception: If unsupported column types are found or schema is invalid

    Example:
        >>> from pg_data_generator.main import generate_data
        >>> tables = generate_data('schema.csv', row_count=100, output_dir='./output')
        >>> print(f"Generated {len(tables)} tables")
    """
    csv = Csv(schema_csv_path, output_dir=output_dir)
    dg = DataGenerator(csv)
    dg.make_csv_for_tables(row_count)
    return csv.table_names


def generate_data_from_ddl_folder(ddl_folder_path, output_data_dir, row_count=10, schema_csv_path=None):
    """
    Convert DDL files to CSV schema and generate synthetic data.

    This function:
    1. Scans the DDL folder for all .sql files
    2. Parses CREATE TABLE statements and FK relationships
    3. Generates a CSV schema file
    4. Generates synthetic data based on the schema

    Args:
        ddl_folder_path (str): Path to folder containing .sql files
        output_data_dir (str): Directory where output data CSV files will be saved
        row_count (int): Number of rows to generate for each table (default: 10)
        schema_csv_path (str): Path to save the generated CSV schema file.
                              If None, saves as 'schema.csv' in output_data_dir (default: None)

    Returns:
        tuple: (list of generated table names, path to schema CSV file)

    Example:
        >>> from pg_data_generator.main import generate_data_from_ddl_folder
        >>> tables, schema = generate_data_from_ddl_folder(
        ...     ddl_folder_path='./sql',
        ...     output_data_dir='./generated_data',
        ...     row_count=100
        ... )
        >>> print(f"Generated {len(tables)} tables using schema: {schema}")
    """
    import os

    # Determine schema CSV path
    if schema_csv_path is None:
        schema_csv_path = os.path.join(output_data_dir, 'schema.csv')

    # Create output directory if it doesn't exist
    if not os.path.exists(output_data_dir):
        os.makedirs(output_data_dir)

    # Convert DDL folder to CSV schema
    print(f"Converting DDL files from: {ddl_folder_path}")
    ddl_folder_to_csv(ddl_folder_path, schema_csv_path)

    # Generate data from CSV schema
    print(f"\nGenerating {row_count} rows per table...")
    tables = generate_data(schema_csv_path, row_count=row_count, output_dir=output_data_dir)

    return tables, schema_csv_path


def generate_data_with_dml(schema_csv_path, row_count=10, output_dir=None,
                           dml_output_dir=None, batch_size=100):
    """
    Generate synthetic data and convert it to SQL INSERT statements.

    This function:
    1. Generates CSV data files from schema
    2. Converts CSV files to SQL INSERT statements (DML)

    Args:
        schema_csv_path (str): Path to the CSV schema file
        row_count (int): Number of rows to generate for each table (default: 10)
        output_dir (str): Directory for CSV output files (default: current directory)
        dml_output_dir (str): Directory for SQL DML files. If None, uses output_dir/sql (default: None)
        batch_size (int): Number of rows per INSERT statement (default: 100)

    Returns:
        dict: Dictionary with keys 'csv_files' (list of CSV paths) and 'dml_files' (list of SQL paths)

    Example:
        >>> from pg_data_generator.main import generate_data_with_dml
        >>> result = generate_data_with_dml(
        ...     'schema.csv',
        ...     row_count=100,
        ...     output_dir='./data',
        ...     dml_output_dir='./sql'
        ... )
        >>> print(f"Generated {len(result['dml_files'])} SQL files")
    """
    import os

    # Generate CSV data
    print(f"Generating {row_count} rows per table...")
    tables = generate_data(schema_csv_path, row_count=row_count, output_dir=output_dir)

    # Determine DML output directory
    if dml_output_dir is None:
        csv_dir = output_dir if output_dir else '.'
        dml_output_dir = os.path.join(csv_dir, 'sql')

    # Convert CSV to DML
    print(f"\nConverting CSV data to SQL INSERT statements...")
    csv_dir = output_dir if output_dir else '.'
    dml_files = csv_folder_to_dml(
        csv_folder_path=csv_dir,
        output_folder_path=dml_output_dir,
        schema_csv_path=schema_csv_path,
        batch_size=batch_size
    )

    return {
        'tables': tables,
        'dml_files': dml_files
    }


def generate_dml_from_ddl_folder(ddl_folder_path, output_dml_dir, row_count=10,
                                  temp_data_dir=None, batch_size=100, keep_temp_files=False):
    """
    Convert DDL files (CREATE TABLE) directly to DML files (INSERT statements).

    This is a complete end-to-end function that:
    1. Parses DDL files (.sql) from the folder
    2. Generates a temporary CSV schema
    3. Generates synthetic data as CSV files
    4. Converts CSV data to SQL INSERT statements
    5. Optionally cleans up temporary files

    Args:
        ddl_folder_path (str): Path to folder containing .sql DDL files
        output_dml_dir (str): Directory where SQL INSERT files will be saved
        row_count (int): Number of rows to generate for each table (default: 10)
        temp_data_dir (str): Directory for temporary CSV files. If None, uses a temp dir (default: None)
        batch_size (int): Number of rows per INSERT statement (default: 100)
        keep_temp_files (bool): If True, keeps temporary CSV files. If False, deletes them (default: False)

    Returns:
        dict: Dictionary with:
              - 'dml_files': List of generated SQL file paths
              - 'tables': List of table names
              - 'schema_path': Path to the schema CSV file (if kept)
              - 'data_dir': Path to the data directory (if kept)

    Example:
        >>> from pg_data_generator.main import generate_dml_from_ddl_folder
        >>> result = generate_dml_from_ddl_folder(
        ...     ddl_folder_path='./sql_schemas',
        ...     output_dml_dir='./insert_statements',
        ...     row_count=100,
        ...     batch_size=50
        ... )
        >>> print(f"Generated {len(result['dml_files'])} SQL INSERT files")
        >>> print(f"Tables: {result['tables']}")
    """
    import os
    import shutil
    import tempfile

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dml_dir):
        os.makedirs(output_dml_dir)

    # Determine temporary data directory
    use_temp_dir = temp_data_dir is None
    if use_temp_dir:
        temp_data_dir = tempfile.mkdtemp(prefix='pg_data_gen_')
        print(f"Using temporary directory: {temp_data_dir}")
    else:
        if not os.path.exists(temp_data_dir):
            os.makedirs(temp_data_dir)

    try:
        # Step 1: Convert DDL to CSV schema and generate data
        print(f"Step 1/3: Converting DDL files and generating data...")
        tables, schema_csv_path = generate_data_from_ddl_folder(
            ddl_folder_path=ddl_folder_path,
            output_data_dir=temp_data_dir,
            row_count=row_count
        )

        # Step 2: Convert CSV data to DML
        print(f"\nStep 2/3: Converting CSV data to SQL INSERT statements...")
        dml_files = csv_folder_to_dml(
            csv_folder_path=temp_data_dir,
            output_folder_path=output_dml_dir,
            schema_csv_path=schema_csv_path,
            batch_size=batch_size
        )

        # Step 3: Cleanup or keep files
        print(f"\nStep 3/3: Finalizing...")
        result = {
            'dml_files': dml_files,
            'tables': tables
        }

        if keep_temp_files:
            result['schema_path'] = schema_csv_path
            result['data_dir'] = temp_data_dir
            print(f"Kept temporary files in: {temp_data_dir}")
        else:
            if use_temp_dir:
                shutil.rmtree(temp_data_dir)
                print(f"Cleaned up temporary files")
            else:
                print(f"Temporary files kept in: {temp_data_dir}")

        print(f"\n✓ Successfully generated {len(dml_files)} DML file(s) for {len(tables)} table(s)")
        return result

    except Exception as e:
        # Clean up on error if we created a temp dir
        if use_temp_dir and not keep_temp_files and os.path.exists(temp_data_dir):
            shutil.rmtree(temp_data_dir)
        raise e


def ddl_to_dml(ddl_file_path, output_dml_dir, row_count=10, batch_size=100, keep_temp_files=False):
    """
    Convert a single DDL file directly to DML INSERT statements.

    This function:
    1. Parses the DDL file containing CREATE TABLE statements
    2. Generates synthetic data based on the schema
    3. Converts the data to SQL INSERT statements

    Args:
        ddl_file_path (str): Path to the SQL/DDL file with CREATE TABLE statements
        output_dml_dir (str): Directory where SQL INSERT files will be saved
        row_count (int): Number of rows to generate for each table (default: 10)
        batch_size (int): Number of rows per INSERT statement (default: 100)
        keep_temp_files (bool): If True, keeps temporary CSV files (default: False)

    Returns:
        dict: Dictionary with:
              - 'dml_files': List of generated SQL file paths
              - 'tables': List of table names
              - 'schema_path': Path to the schema CSV (if kept)
              - 'data_dir': Path to the data directory (if kept)

    Example:
        >>> from pg_data_generator.main import ddl_to_dml
        >>> result = ddl_to_dml(
        ...     ddl_file_path='./schema.sql',
        ...     output_dml_dir='./insert_statements',
        ...     row_count=100
        ... )
        >>> print(f"Generated {len(result['dml_files'])} INSERT files")
    """
    import os
    import tempfile
    import shutil

    # Create a temporary folder with just this DDL file
    temp_ddl_dir = tempfile.mkdtemp(prefix='pg_ddl_')
    try:
        # Copy DDL file to temp directory
        ddl_filename = os.path.basename(ddl_file_path)
        temp_ddl_path = os.path.join(temp_ddl_dir, ddl_filename)
        shutil.copy2(ddl_file_path, temp_ddl_path)

        # Use the folder-based function
        result = generate_dml_from_ddl_folder(
            ddl_folder_path=temp_ddl_dir,
            output_dml_dir=output_dml_dir,
            row_count=row_count,
            batch_size=batch_size,
            keep_temp_files=keep_temp_files
        )

        return result

    finally:
        # Clean up temporary DDL directory
        if os.path.exists(temp_ddl_dir):
            shutil.rmtree(temp_ddl_dir)


# Public API exports
__all__ = [
    # Core data generation functions
    'generate_data',
    'generate_data_from_ddl_folder',
    'generate_data_with_dml',

    # DDL to DML conversion (CREATE to INSERT)
    'generate_dml_from_ddl_folder',
    'ddl_to_dml',

    # DDL to CSV schema conversion
    'ddl_to_csv',
    'ddl_folder_to_csv',
    'ddl_string_to_csv',

    # CSV to DML conversion
    'csv_to_dml',
    'csv_folder_to_dml',
]
