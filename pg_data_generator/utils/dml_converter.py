"""
DML Generator - CSV to SQL INSERT Statements

This module converts generated CSV data files into SQL INSERT statements (DML).
It reads CSV files and table schema to generate proper SQL INSERT statements
with correct data types and quoting.
"""

import csv
import os
from typing import List, Dict, Optional


def csv_to_dml(csv_file_path: str, table_name: str, output_sql_path: str,
               batch_size: int = 100, schema_info: Optional[Dict] = None) -> None:
    """
    Convert a single CSV file to SQL INSERT statements.

    Args:
        csv_file_path (str): Path to the CSV data file
        table_name (str): Name of the table for INSERT statements
        output_sql_path (str): Path to output SQL file
        batch_size (int): Number of rows per INSERT statement (default: 100)
        schema_info (dict): Optional schema information with column types
                           Format: {'column_name': 'type', ...}

    Example:
        >>> csv_to_dml('MST_CUSTOMER.csv', 'MST_CUSTOMER', 'insert_customer.sql')
    """
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        if not rows:
            print(f"Warning: No data found in {csv_file_path}")
            return

        column_names = list(rows[0].keys())

        with open(output_sql_path, 'w', encoding='utf-8') as sqlfile:
            # Write header comment
            sqlfile.write(f"-- INSERT statements for {table_name}\n")
            sqlfile.write(f"-- Generated from: {os.path.basename(csv_file_path)}\n")
            sqlfile.write(f"-- Total rows: {len(rows)}\n\n")

            # Generate batched INSERT statements
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                insert_sql = _generate_insert_statement(
                    table_name,
                    column_names,
                    batch,
                    schema_info
                )
                sqlfile.write(insert_sql)
                sqlfile.write("\n\n")

    print(f"Generated INSERT statements: {output_sql_path}")


def csv_folder_to_dml(csv_folder_path: str, output_folder_path: str,
                      schema_csv_path: Optional[str] = None,
                      batch_size: int = 100) -> List[str]:
    """
    Convert all CSV files in a folder to DML SQL files.

    This function:
    1. Finds all CSV files in the folder (excluding schema.csv)
    2. Optionally loads schema information for proper type handling
    3. Generates SQL INSERT statements for each CSV file

    Args:
        csv_folder_path (str): Path to folder containing CSV data files
        output_folder_path (str): Path to folder for output SQL files
        schema_csv_path (str): Optional path to schema.csv for type information
        batch_size (int): Number of rows per INSERT statement (default: 100)

    Returns:
        List[str]: List of generated SQL file paths

    Example:
        >>> files = csv_folder_to_dml('./generated_data', './sql_inserts')
        >>> print(f"Generated {len(files)} DML files")
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Load schema information if provided
    schema_map = {}
    if schema_csv_path and os.path.exists(schema_csv_path):
        schema_map = _load_schema_info(schema_csv_path)

    # Find all CSV files (excluding schema.csv)
    csv_files = []
    for file in os.listdir(csv_folder_path):
        if file.endswith('.csv') and file.lower() != 'schema.csv':
            csv_files.append(file)

    if not csv_files:
        print(f"Warning: No CSV data files found in {csv_folder_path}")
        return []

    print(f"Found {len(csv_files)} CSV file(s) to convert:")
    generated_files = []

    for csv_file in csv_files:
        # Extract table name from filename (remove .csv and any numeric suffix)
        table_name = os.path.splitext(csv_file)[0]
        # Remove trailing numbers (e.g., MST_CUSTOMER1 -> MST_CUSTOMER)
        import re
        table_name = re.sub(r'\d+$', '', table_name)

        csv_path = os.path.join(csv_folder_path, csv_file)
        sql_file = f"{os.path.splitext(csv_file)[0]}_insert.sql"
        sql_path = os.path.join(output_folder_path, sql_file)

        print(f"  - Converting {csv_file} -> {sql_file}")

        # Get schema info for this table
        table_schema = schema_map.get(table_name, {})

        csv_to_dml(csv_path, table_name, sql_path, batch_size, table_schema)
        generated_files.append(sql_path)

    print(f"\nSuccessfully generated {len(generated_files)} DML file(s)")
    return generated_files


def _load_schema_info(schema_csv_path: str) -> Dict[str, Dict[str, str]]:
    """
    Load schema information from CSV file.

    Returns:
        Dict mapping table_name -> {column_name: type}
    """
    schema_map = {}

    with open(schema_csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            table_name = row['table_name']
            column_name = row['column']
            column_type = row['type'].upper()

            if table_name not in schema_map:
                schema_map[table_name] = {}

            schema_map[table_name][column_name] = column_type

    return schema_map


def _generate_insert_statement(table_name: str, column_names: List[str],
                               rows: List[Dict], schema_info: Optional[Dict] = None) -> str:
    """
    Generate a single INSERT statement for a batch of rows.

    Args:
        table_name (str): Table name
        column_names (List[str]): List of column names
        rows (List[Dict]): List of row data
        schema_info (dict): Optional schema with column types

    Returns:
        str: SQL INSERT statement
    """
    # Start INSERT statement
    columns_str = ', '.join(column_names)
    sql_parts = [f"INSERT INTO {table_name} ({columns_str})"]
    sql_parts.append("VALUES")

    # Generate value rows
    value_rows = []
    for row in rows:
        values = []
        for col_name in column_names:
            value = row.get(col_name, '')
            formatted_value = _format_sql_value(value, col_name, schema_info)
            values.append(formatted_value)

        values_str = ', '.join(values)
        value_rows.append(f"    ({values_str})")

    sql_parts.append(',\n'.join(value_rows))
    sql_parts.append(";")

    return '\n'.join(sql_parts)


def _format_sql_value(value: str, column_name: str, schema_info: Optional[Dict] = None) -> str:
    """
    Format a value for SQL INSERT statement based on its type.

    Args:
        value (str): The value to format
        column_name (str): Name of the column
        schema_info (dict): Optional schema information

    Returns:
        str: Formatted SQL value
    """
    # Handle NULL values
    if value == '' or value is None:
        return 'NULL'

    # Determine column type
    col_type = None
    if schema_info and column_name in schema_info:
        col_type = schema_info[column_name].upper()

    # Numeric types - no quotes
    if col_type:
        if any(t in col_type for t in ['INT', 'BIGINT', 'SMALLINT', 'DECIMAL', 'NUMERIC', 'FLOAT', 'REAL', 'DOUBLE']):
            return str(value)

    # Date/Time types - single quotes
    if col_type:
        if any(t in col_type for t in ['DATE', 'TIME', 'TIMESTAMP']):
            # Escape single quotes in value
            escaped_value = value.replace("'", "''")
            return f"'{escaped_value}'"

    # String types (VARCHAR, CHAR, TEXT, etc.) - single quotes
    # This is also the default for unknown types
    escaped_value = value.replace("'", "''")
    return f"'{escaped_value}'"


def generate_dml_from_data_folder(data_folder_path: str, output_dml_folder: str,
                                  schema_csv_path: Optional[str] = None,
                                  batch_size: int = 100) -> List[str]:
    """
    Convenience function to generate DML files from a data folder.

    This is an alias for csv_folder_to_dml with more explicit naming.

    Args:
        data_folder_path (str): Path to folder with CSV data files
        output_dml_folder (str): Path to folder for SQL output files
        schema_csv_path (str): Optional path to schema.csv
        batch_size (int): Rows per INSERT statement

    Returns:
        List[str]: List of generated SQL file paths
    """
    return csv_folder_to_dml(data_folder_path, output_dml_folder, schema_csv_path, batch_size)
