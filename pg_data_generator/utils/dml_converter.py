import csv
import os
from typing import List, Dict, Optional


def csv_to_dml(csv_file_path: str, table_name: str, output_sql_path: str,
               batch_size: int = 100, schema_info: Optional[Dict] = None) -> None:
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

        if not rows:
            print(f"Warning: No data found in {csv_file_path}")
            return

        column_names = list(rows[0].keys())

        with open(output_sql_path, 'w', encoding='utf-8') as sqlfile:
            sqlfile.write(f"-- INSERT statements for {table_name}\n")
            sqlfile.write(f"-- Generated from: {os.path.basename(csv_file_path)}\n")
            sqlfile.write(f"-- Total rows: {len(rows)}\n\n")

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
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    schema_map = {}
    if schema_csv_path and os.path.exists(schema_csv_path):
        schema_map = _load_schema_info(schema_csv_path)

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
        table_name = os.path.splitext(csv_file)[0]

        import re
        table_name = re.sub(r'\d+$', '', table_name)

        csv_path = os.path.join(csv_folder_path, csv_file)
        sql_file = f"{os.path.splitext(csv_file)[0]}_insert.sql"
        sql_path = os.path.join(output_folder_path, sql_file)

        print(f"  - Converting {csv_file} -> {sql_file}")

        table_schema = schema_map.get(table_name, {})

        csv_to_dml(csv_path, table_name, sql_path, batch_size, table_schema)
        generated_files.append(sql_path)

    print(f"\nSuccessfully generated {len(generated_files)} DML file(s)")
    return generated_files


def _load_schema_info(schema_csv_path: str) -> Dict[str, Dict[str, str]]:
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
    columns_str = ', '.join(column_names)
    sql_parts = [f"INSERT INTO {table_name} ({columns_str})"]
    sql_parts.append("VALUES")

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
    if value == '' or value is None:
        return 'NULL'

    col_type = None
    if schema_info and column_name in schema_info:
        col_type = schema_info[column_name].upper()

    if col_type:
        if any(t in col_type for t in ['INT', 'BIGINT', 'SMALLINT', 'DECIMAL', 'NUMERIC', 'FLOAT', 'REAL', 'DOUBLE']):
            return str(value)

    if col_type:
        if any(t in col_type for t in ['DATE', 'TIME', 'TIMESTAMP']):
            escaped_value = value.replace("'", "''")
            return f"'{escaped_value}'"

    escaped_value = value.replace("'", "''")
    return f"'{escaped_value}'"
