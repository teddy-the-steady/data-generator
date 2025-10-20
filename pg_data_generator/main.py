"""
Main API module for pg-data-generator.

This module provides the public API for generating synthetic PostgreSQL data
from CSV schema definitions. Use this when importing the package from other repositories.
"""

from pg_data_generator.core.Csv import Csv
from pg_data_generator.core.DataGenerator import DataGenerator


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
