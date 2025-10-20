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


# Re-export converter functions for convenience
__all__ = [
    'generate_data',
    'generate_data_from_schema',
    'generate_data_from_ddl_folder',
    'ddl_to_csv',
    'ddl_folder_to_csv',
    'ddl_string_to_csv'
]
