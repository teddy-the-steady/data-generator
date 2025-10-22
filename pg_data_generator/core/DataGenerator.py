from pg_data_generator.cases.Optional import Optional
from pg_data_generator.cases.Name import Name
from pg_data_generator.cases.Address import Address
from pg_data_generator.cases.Int import Int
from pg_data_generator.cases.Decimal import Decimal
from pg_data_generator.cases.Year import Year
from pg_data_generator.cases.PhoneNumber import PhoneNumber
from pg_data_generator.cases.DateTime import DateTime
from pg_data_generator.cases.Code import Code
from pg_data_generator.cases.Email import Email
from pg_data_generator.cases.Varchar import Varchar
from pg_data_generator.cases.Etc import Etc

from pg_data_generator.core.Csv import Csv
from pg_data_generator.core.Fk_handler import FKHandler

class DataGenerator():
    def __init__(self, csv):
        self.csv = csv
        self.unsupported_columns = list()
        # Initialize FK handler for enforcing foreign key relationships
        self.fk_handler = FKHandler(csv.tables, csv.output_dir)


    def make_csv_for_tables(self, count):
        # Get tables in correct dependency order (FK enforcement)
        table_order = self.fk_handler.get_table_generation_order()
        print(f"Table generation order (respecting FK dependencies): {table_order}")

        for table_name in table_order:
            try:
                print(f"Generating data for table: {table_name}")
                self._make_data_for_table(table_name, count)
            except Exception as e:
                raise Exception(f"Error generating data for table '{table_name}': {str(e)}") from e

        if len(self.unsupported_columns) > 0:
            raise Exception(f'Unsupported columns found: {self.unsupported_columns}')


    def _make_data_for_table(self, table_name, count):
        # TODO
        # 1. make sets of each column
        index = Csv.index_of_table(self.csv.tables, table_name)
        original_table_name = table_name
        table_name = self.csv.prepare_next_file_name(table_name)

        for column_metadata in self.csv.tables[index].columns:
            try:
                result = self._generate_column_items(count, column_metadata)

                self.csv.write_results_to_csv(
                    column_metadata['column'],
                    result,
                    table_name
                )
            except Exception as e:
                raise Exception(
                    f"Error generating column '{column_metadata['column']}' "
                    f"(type: {column_metadata.get('type', 'unknown')}): {str(e)}"
                ) from e

        #   a. check format (options, code, hankaku, email? and more)
        #   b. consider length + type
        #   c. check constraint (unique=true, pk=true)
        #   d. use random function (+ set)
        # 2. combine list(set) of columns to make rows
        # 3. decide how to deal with FK situation!!!!
        # >> after making up all the columns and then give correction
        # >> when insert, consider the order of tables referring and referred
        # 4. export result to csv file


    def _generate_column_items(self, count, column_metadata):
        # Check if this is a PK column - if so, generate sequential unique integers
        constraint = column_metadata.get('constraint', '')
        if constraint == 'pk':
            # Generate sequential integers starting from 1
            return [str(i) for i in range(1, count + 1)]

        # Check if this is a FK column - if so, get values from referenced table
        if self.fk_handler.is_fk_column(column_metadata):
            try:
                referenced_table, referenced_column = self.fk_handler.parse_fk_constraint(constraint)
                return self.fk_handler.get_fk_values(referenced_table, referenced_column, count)
            except Exception as e:
                raise Exception(
                    f"FK constraint error for column '{column_metadata['column']}' "
                    f"(constraint: {constraint}): {str(e)}"
                )

        if Optional.has_optional_choice(column_metadata['format']):
            result = Optional(count, column_metadata)
            return result.make_column()

        if Name.is_name(column_metadata['column']):
            result = Name(count, column_metadata)
            return result.make_column()

        if Email.is_email(column_metadata['column']):
            result = Email(count, column_metadata)
            return result.make_column()

        if Address.is_address(column_metadata['column']):
            result = Address(count, column_metadata)
            return result.make_column()

        if DateTime.is_date_or_datetime(column_metadata['type']):
            result = DateTime(count, column_metadata)
            return result.make_column()

        if PhoneNumber.is_phone_number(column_metadata['column']):
            result = PhoneNumber(count, column_metadata)
            return result.make_column()

        if Year.is_year(column_metadata['column']):
            result = Year(count, column_metadata)
            return result.make_column()

        if Int.is_int(column_metadata['type']):
            result = Int(count, column_metadata)
            return result.make_column()

        if Decimal.is_decimal(column_metadata['type']):
            result = Decimal(count, column_metadata)
            return result.make_column()

        if Code.is_code(column_metadata['column']):
            result = Code(count, column_metadata)
            return result.make_column()

        if Varchar.is_varchar(column_metadata['type']):
            result = Varchar(count, column_metadata)
            return result.make_column()

        if Etc.is_etc(column_metadata['column']):
            result = Etc(count, column_metadata)
            return result.make_column()

        self.unsupported_columns.append(column_metadata['column'])
