"""
Foreign Key Handler Module

This module handles foreign key enforcement during data generation:
1. Determines correct table generation order (topological sort)
2. Provides FK values from referenced tables
"""

from typing import List, Dict, Set, Optional
import pandas as pd
import os


class FKHandler:
    """Handles foreign key relationships and enforcement."""

    def __init__(self, tables: List, output_dir: str):
        """
        Initialize FK handler.

        Args:
            tables: List of Table objects with columns and foreign_keys
            output_dir: Directory where CSV files are being written
        """
        self.tables = tables
        self.output_dir = output_dir
        self.table_dict = {table.table_name: table for table in tables}
        self.generated_data = {}  # Cache of generated table data

    def get_table_generation_order(self) -> List[str]:
        """
        Determine the order in which tables should be generated.
        Uses topological sort to ensure referenced tables are generated first.

        Returns:
            List of table names in generation order

        Raises:
            Exception: If circular dependencies are detected
        """
        # Build dependency graph
        dependencies = {}  # table_name -> set of tables it depends on

        for table in self.tables:
            table_name = table.table_name
            dependencies[table_name] = set()

            # Check each column for FK references
            for column in table.columns:
                constraint = column.get('constraint', '')
                if constraint.startswith('fk.'):
                    # Parse fk.REFERENCED_TABLE.referenced_column
                    parts = constraint.split('.')
                    if len(parts) >= 2:
                        referenced_table = parts[1]
                        if referenced_table != table_name:  # Not self-reference
                            dependencies[table_name].add(referenced_table)

        # Topological sort using Kahn's algorithm
        # in_degree represents how many dependencies each table has (outgoing edges)
        in_degree = {table: len(dependencies[table]) for table in dependencies}

        # Find tables with no dependencies (in_degree == 0)
        queue = [table for table, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            # Sort to ensure deterministic order
            queue.sort()
            current_table = queue.pop(0)
            result.append(current_table)

            # For each table that depends on tables NOT YET processed
            for table in dependencies:
                # If this table depends on the current_table we just processed
                if current_table in dependencies[table]:
                    # Reduce its dependency count
                    in_degree[table] -= 1
                    # If all dependencies satisfied, add to queue
                    if in_degree[table] == 0:
                        queue.append(table)

        # Check for circular dependencies
        if len(result) != len(dependencies):
            missing = set(dependencies.keys()) - set(result)
            raise Exception(
                f"Circular dependency detected among tables: {missing}. "
                "Cannot generate data with circular foreign key references."
            )

        return result

    def get_fk_values(self, referenced_table: str, referenced_column: str, count: int) -> List[str]:
        """
        Get valid FK values from a referenced table's column.

        Args:
            referenced_table: Name of the table being referenced
            referenced_column: Name of the column being referenced
            count: Number of values needed

        Returns:
            List of valid FK values (randomly selected with replacement)

        Raises:
            Exception: If referenced table hasn't been generated yet
        """
        import random

        # Check if we have cached data
        if referenced_table not in self.generated_data:
            # Try to load from CSV file
            csv_path = self._find_table_csv(referenced_table)
            if not csv_path:
                raise Exception(
                    f"Cannot find generated data for referenced table '{referenced_table}'. "
                    f"Ensure tables are generated in dependency order."
                )

            # Load the data
            df = pd.read_csv(csv_path, dtype=str)
            self.generated_data[referenced_table] = df

        # Get the referenced column data
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

        # Randomly select values with replacement
        return [str(random.choice(available_values)) for _ in range(count)]

    def _find_table_csv(self, table_name: str) -> Optional[str]:
        """
        Find the CSV file for a given table.

        Args:
            table_name: Name of the table

        Returns:
            Path to CSV file, or None if not found
        """
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
        """
        Check if a column is a foreign key.

        Args:
            column_metadata: Column metadata dictionary

        Returns:
            True if column is a FK, False otherwise
        """
        constraint = column_metadata.get('constraint', '')
        return constraint.startswith('fk.')

    def parse_fk_constraint(self, constraint: str) -> tuple:
        """
        Parse FK constraint string.

        Args:
            constraint: FK constraint string (e.g., "fk.MST_EXAMPLE.id")

        Returns:
            Tuple of (referenced_table, referenced_column)

        Raises:
            ValueError: If constraint format is invalid
        """
        parts = constraint.split('.')
        if len(parts) < 3 or parts[0] != 'fk':
            raise ValueError(f"Invalid FK constraint format: {constraint}")

        referenced_table = parts[1]
        referenced_column = parts[2]
        return referenced_table, referenced_column