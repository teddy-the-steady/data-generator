from typing import List, Dict, Set, Optional
import pandas as pd
import os


class FKHandler:
    def __init__(self, tables: List, output_dir: str):
        self.tables = tables
        self.output_dir = output_dir
        self.table_dict = {table.table_name: table for table in tables}
        self.generated_data = {}  # Cache of generated table data

    def get_table_generation_order(self) -> List[str]:
        # Build dependency graph
        dependencies = {}  # table_name -> set of tables it depends on

        for table in self.tables:
            table_name = table.table_name
            dependencies[table_name] = set()

            for column in table.columns:
                constraint = column.get('constraint', '')
                if constraint.startswith('fk.'):
                    parts = constraint.split('.')
                    if len(parts) >= 2:
                        referenced_table = parts[1]
                        if referenced_table != table_name:  # Not self-reference
                            dependencies[table_name].add(referenced_table)

        in_degree = {table: len(dependencies[table]) for table in dependencies}

        queue = [table for table, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            queue.sort()
            current_table = queue.pop(0)
            result.append(current_table)

            for table in dependencies:
                if current_table in dependencies[table]:
                    in_degree[table] -= 1
                    if in_degree[table] == 0:
                        queue.append(table)

        if len(result) != len(dependencies):
            missing = set(dependencies.keys()) - set(result)
            raise Exception(
                f"Circular dependency detected among tables: {missing}. "
                "Cannot generate data with circular foreign key references."
            )

        return result

    def get_fk_values(self, referenced_table: str, referenced_column: str, count: int) -> List[str]:
        import random

        if referenced_table not in self.generated_data:
            csv_path = self._find_table_csv(referenced_table)
            if not csv_path:
                raise Exception(
                    f"Cannot find generated data for referenced table '{referenced_table}'. "
                    f"Ensure tables are generated in dependency order."
                )

            df = pd.read_csv(csv_path, dtype=str)
            self.generated_data[referenced_table] = df

        df = self.generated_data[referenced_table]
        if referenced_column not in df.columns:
            raise Exception(
                f"Referenced column '{referenced_column}' not found in table '{referenced_table}'"
            )

        available_values = df[referenced_column].dropna().tolist()

        if not available_values:
            raise Exception(
                f"No values available in {referenced_table}.{referenced_column} for FK reference"
            )

        return [str(random.choice(available_values)) for _ in range(count)]

    def _find_table_csv(self, table_name: str) -> Optional[str]:
        # Try exact match first
        csv_path = os.path.join(self.output_dir, f"{table_name}.csv")
        if os.path.exists(csv_path):
            return csv_path

        # Try with numeric suffix (table1.csv, table2.csv, etc.)
        for i in range(1, 100):
            csv_path = os.path.join(self.output_dir, f"{table_name}{i}.csv")
            if os.path.exists(csv_path):
                return csv_path

        return None

    def is_fk_column(self, column_metadata: Dict) -> bool:
        constraint = column_metadata.get('constraint', '')
        return constraint.startswith('fk.')

    def parse_fk_constraint(self, constraint: str) -> tuple:
        parts = constraint.split('.')
        if len(parts) < 3 or parts[0] != 'fk':
            raise ValueError(f"Invalid FK constraint format: {constraint}")

        referenced_table = parts[1]
        referenced_column = parts[2]
        return referenced_table, referenced_column