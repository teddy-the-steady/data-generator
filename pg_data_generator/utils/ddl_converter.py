import re
import csv
import os
from typing import List, Dict, Optional


def ddl_folder_to_csv(folder_path: str, output_csv_path: str) -> None:
    sql_files = []
    for file in os.listdir(folder_path):
        if file.endswith('.sql'):
            sql_files.append(os.path.join(folder_path, file))

    if not sql_files:
        raise ValueError(f"No .sql files found in {folder_path}")

    print(f"Found {len(sql_files)} SQL file(s):")
    for sql_file in sql_files:
        print(f"  - {os.path.basename(sql_file)}")

    all_tables = []
    for sql_file in sql_files:
        tables = parse_ddl_file(sql_file)
        all_tables.extend(tables)

    print(f"\nParsed {len(all_tables)} table(s)")

    write_csv_schema(all_tables, output_csv_path)
    print(f"Successfully created: {output_csv_path}")


def parse_ddl_file(ddl_file_path: str) -> List[Dict]:
    with open(ddl_file_path, 'r', encoding='utf-8') as f:
        ddl_content = f.read()

    return parse_ddl_string(ddl_content)


def parse_ddl_string(ddl_content: str) -> List[Dict]:
    tables = []

    ddl_content = re.sub(r'--[^\n]*', '', ddl_content)
    ddl_content = re.sub(r'/\*.*?\*/', '', ddl_content, flags=re.DOTALL)

    create_table_pattern = re.compile(
        r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([^\s(]+)\s*\((.*?)\);',
        re.IGNORECASE | re.DOTALL
    )

    for match in create_table_pattern.finditer(ddl_content):
        table_name = match.group(1).strip().strip('"').strip('`').strip('[]')
        columns_def = match.group(2).strip()

        table_info = {
            'table_name': table_name,
            'columns': [],
            'foreign_keys': {}
        }

        column_defs = _split_column_definitions(columns_def)

        primary_keys = []
        foreign_keys = {}

        for col_def in column_defs:
            col_def = col_def.strip()

            pk_match = re.match(r'PRIMARY\s+KEY\s*\(([^)]+)\)', col_def, re.IGNORECASE)
            if pk_match:
                pk_cols = [c.strip().strip('"').strip('`').strip('[]') for c in pk_match.group(1).split(',')]
                primary_keys.extend(pk_cols)
                continue

            fk_match = re.match(
                r'FOREIGN\s+KEY\s*\(([^)]+)\)\s+REFERENCES\s+([^\s(]+)\s*\(([^)]+)\)',
                col_def,
                re.IGNORECASE
            )
            if fk_match:
                fk_col = fk_match.group(1).strip().strip('"').strip('`').strip('[]')
                ref_table = fk_match.group(2).strip().strip('"').strip('`').strip('[]')
                ref_col = fk_match.group(3).strip().strip('"').strip('`').strip('[]')
                foreign_keys[fk_col] = (ref_table, ref_col)
                continue

            unique_match = re.match(r'UNIQUE\s*\(([^)]+)\)', col_def, re.IGNORECASE)
            if unique_match:
                # Skip UNIQUE constraints - we don't enforce uniqueness during generation
                continue

            check_match = re.match(r'CHECK\s*\(', col_def, re.IGNORECASE)
            if check_match:
                # Skip CHECK constraints
                continue

            if re.match(r'CONSTRAINT\s+', col_def, re.IGNORECASE):
                constraint_match = re.match(
                    r'CONSTRAINT\s+\S+\s+(.*)',
                    col_def,
                    re.IGNORECASE
                )
                if constraint_match:
                    constraint_content = constraint_match.group(1)

                    pk_match = re.match(r'PRIMARY\s+KEY\s*\(([^)]+)\)', constraint_content, re.IGNORECASE)
                    if pk_match:
                        pk_cols = [c.strip().strip('"').strip('`').strip('[]') for c in pk_match.group(1).split(',')]
                        primary_keys.extend(pk_cols)
                        continue

                    unique_match = re.match(r'UNIQUE\s*\(([^)]+)\)', constraint_content, re.IGNORECASE)
                    if unique_match:
                        # Skip UNIQUE constraints
                        continue

                    check_match = re.match(r'CHECK\s*\(', constraint_content, re.IGNORECASE)
                    if check_match:
                        # Skip CHECK constraints
                        continue

                    fk_match = re.match(
                        r'FOREIGN\s+KEY\s*\(([^)]+)\)\s+REFERENCES\s+([^\s(]+)\s*\(([^)]+)\)',
                        constraint_content,
                        re.IGNORECASE
                    )
                    if fk_match:
                        fk_col = fk_match.group(1).strip().strip('"').strip('`').strip('[]')
                        ref_table = fk_match.group(2).strip().strip('"').strip('`').strip('[]')
                        ref_col = fk_match.group(3).strip().strip('"').strip('`').strip('[]')
                        foreign_keys[fk_col] = (ref_table, ref_col)
                        continue

                # If it's a CONSTRAINT but not one we recognize, skip it
                continue

            column_info = _parse_column_definition(col_def)
            if column_info:
                if column_info.get('is_primary_key'):
                    primary_keys.append(column_info['name'])

                if column_info.get('foreign_key'):
                    fk_table, fk_col = column_info['foreign_key']
                    foreign_keys[column_info['name']] = (fk_table, fk_col)

                table_info['columns'].append(column_info)

        for col in table_info['columns']:
            if col['name'] in primary_keys:
                col['is_primary_key'] = True

        for col in table_info['columns']:
            if col['name'] in foreign_keys:
                ref_table, ref_col = foreign_keys[col['name']]
                col['foreign_key'] = (ref_table, ref_col)

        table_info['foreign_keys'] = foreign_keys
        tables.append(table_info)

    return tables


def _split_column_definitions(columns_def: str) -> List[str]:
    parts = []
    current = []
    paren_depth = 0

    for char in columns_def:
        if char == '(':
            paren_depth += 1
            current.append(char)
        elif char == ')':
            paren_depth -= 1
            current.append(char)
        elif char == ',' and paren_depth == 0:
            parts.append(''.join(current))
            current = []
        else:
            current.append(char)

    if current:
        parts.append(''.join(current))

    return parts


def _parse_column_definition(col_def: str) -> Optional[Dict]:
    col_pattern = re.match(
        r'^\s*([^\s]+)\s+([^\s(]+(?:\([^)]+\))?)(.*)',
        col_def,
        re.IGNORECASE
    )

    if not col_pattern:
        return None

    col_name = col_pattern.group(1).strip().strip('"').strip('`').strip('[]')
    col_type = col_pattern.group(2).strip().upper()
    col_constraints = col_pattern.group(3).strip()

    type_match = re.match(r'([^\(]+)(?:\((\d+)(?:,\s*(\d+))?\))?', col_type)
    if not type_match:
        return None

    base_type = type_match.group(1).strip()
    length = type_match.group(2)
    precision = type_match.group(3)  # For DECIMAL(15,2)

    if precision:
        full_type = f"{base_type}({length},{precision})"
    elif length and base_type not in ['INT', 'BIGINT', 'SMALLINT', 'DATE', 'DATETIME', 'TIMESTAMP']:
        full_type = f"{base_type}({length})"
    else:
        full_type = base_type

    is_primary_key = bool(re.search(r'PRIMARY\s+KEY', col_constraints, re.IGNORECASE))

    foreign_key = None
    fk_match = re.search(
        r'REFERENCES\s+([^\s(]+)\s*\(([^)]+)\)',
        col_constraints,
        re.IGNORECASE
    )
    if fk_match:
        ref_table = fk_match.group(1).strip().strip('"').strip('`').strip('[]')
        ref_col = fk_match.group(2).strip().strip('"').strip('`').strip('[]')
        foreign_key = (ref_table, ref_col)

    return {
        'name': col_name,
        'type': full_type,
        'length': length if length else '',
        'is_primary_key': is_primary_key,
        'foreign_key': foreign_key
    }


def ddl_to_csv(ddl_file_path: str, output_csv_path: str) -> None:
    tables = parse_ddl_file(ddl_file_path)
    write_csv_schema(tables, output_csv_path)


def write_csv_schema(tables: List[Dict], output_csv_path: str) -> None:
    if os.path.exists(output_csv_path) and os.path.isdir(output_csv_path):
        output_csv_path = os.path.join(output_csv_path, 'schema.csv')
        print(f"Output path is a directory. Creating schema file: {output_csv_path}")

    output_dir = os.path.dirname(output_csv_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Use QUOTE_MINIMAL to avoid quoting DECIMAL types with commas
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['table_name', 'column', 'type', 'constraint', 'length', 'format'])

        for table in tables:
            for col in table['columns']:
                table_name = table['table_name']
                col_name = col['name']
                col_type = col['type']
                length = col.get('length', '')
                constraint = ''
                format_val = ''

                if col.get('is_primary_key'):
                    constraint = 'pk'
                elif col.get('foreign_key'):
                    ref_table, ref_col = col['foreign_key']
                    constraint = f'fk.{ref_table}.{ref_col}'

                writer.writerow([
                    table_name,
                    col_name,
                    col_type,
                    constraint,
                    length,
                    format_val
                ])


def ddl_string_to_csv(ddl_string: str, output_csv_path: str) -> None:
    tables = parse_ddl_string(ddl_string)
    write_csv_schema(tables, output_csv_path)
