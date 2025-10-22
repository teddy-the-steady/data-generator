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
    csv_folder_to_dml,
    generate_dml_from_data_folder
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


def generate_data_from_schema(schema_csv_path, output_dir, row_count=10):
    """
    Generate synthetic data with explicit output directory.

    This is an alias for generate_data() with more explicit parameter ordering
    for external repository usage.

    Args:
        schema_csv_path (str): Path to the CSV schema file
        output_dir (str): Directory where output CSV files will be saved
        row_count (int): Number of rows to generate for each table (default: 10)

    Returns:
        list: List of generated table names
    """
    return generate_data(schema_csv_path, row_count=row_count, output_dir=output_dir)


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


def generate_dml_from_csv_folder(csv_folder_path, output_dml_folder,
                                 schema_csv_path=None, batch_size=100):
    """
    Convert existing CSV data files to SQL INSERT statements.

    Use this when you already have generated CSV files and want to create DML files.

    Args:
        csv_folder_path (str): Path to folder containing CSV data files
        output_dml_folder (str): Path to folder for SQL DML output files
        schema_csv_path (str): Optional path to schema.csv for type information (default: None)
        batch_size (int): Number of rows per INSERT statement (default: 100)

    Returns:
        list: List of generated SQL file paths

    Example:
        >>> from pg_data_generator.main import generate_dml_from_csv_folder
        >>> dml_files = generate_dml_from_csv_folder(
        ...     csv_folder_path='./data',
        ...     output_dml_folder='./sql',
        ...     schema_csv_path='./data/schema.csv'
        ... )
        >>> print(f"Generated {len(dml_files)} DML files")
    """
    return csv_folder_to_dml(csv_folder_path, output_dml_folder, schema_csv_path, batch_size)


# Re-export converter functions for convenience
__all__ = [
    'generate_data',
    'generate_data_from_schema',
    'generate_data_from_ddl_folder',
    'generate_data_with_dml',
    'generate_dml_from_csv_folder',
    'ddl_to_csv',
    'ddl_folder_to_csv',
    'ddl_string_to_csv',
    'csv_to_dml',
    'csv_folder_to_dml',
    'generate_dml_from_data_folder'
]
