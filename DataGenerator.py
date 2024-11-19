import os
from glob import glob

from Cases.Optional import Optional
from Cases.Name import Name
from Cases.Address import Address
from Cases.Number import Number
from Cases.PhoneNumber import PhoneNumber
from Cases.DateTime import DateTime
from Cases.Code import Code
from Cases.Email import Email
from Cases.Etc import Etc

from Csv import Csv

RESULT_PATH = 'results'

class DataGenerator():
    possible_pair_columns = {}

    def __init__(self, csv):
        self.csv = csv
        self.unsupported_columns = list()


    def make_csv_for_tables(self, count):
        for table_name in self.csv.table_names:
            self._make_data_for_table(table_name, count)

        if len(self.unsupported_columns) > 0:
            raise Exception(f'Unsupported columns found: {self.unsupported_columns}')


    def _make_data_for_table(self, table_name, count):
        # TODO
        # 1. make sets of each column
        index = Csv.index_of_table(self.csv.tables, table_name)
        table_name = self._prepare_next_file_name(table_name)

        for column_metadata in self.csv.tables[index].columns:
            result = self._generate_column_items(count, column_metadata)

            self.csv.write_results_to_csv(
                column_metadata['column'],
                result,
                f'{RESULT_PATH}/{table_name}.csv'
            )

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
        column_name = column_metadata['column'].lower()
        column_type = column_metadata['type'].lower()

        if Optional.has_optional_choice(column_metadata['format']):
            result = Optional(count, column_metadata)
            return result.make_column()

        if Name.is_name(column_name):
            result = Name(count, column_metadata)
            return result.make_column()

        if Email.is_email(column_name):
            result = Email(count, column_metadata)
            return result.make_column()

        if Address.is_address(column_name):
            result = Address(count, column_metadata)
            return result.make_column()

        if DateTime.is_date_or_datetime(column_type):
            result = DateTime(count, column_metadata)
            return result.make_column()

        if Number.is_number(column_name, column_type):
            if PhoneNumber.is_phone_number(column_name):
                result = PhoneNumber(count, column_metadata)
                return result.make_column()
            else:
                result = Number(count, column_metadata)
                return result.make_column()

        if Code.is_code(column_name):
            result = Code(count, column_metadata)
            return result.make_column()

        if Etc.is_etc(column_name):
            result = Etc(count, column_metadata)
            return result.make_column()

        self.unsupported_columns.append(column_metadata['column'])


    def _prepare_next_file_name(self, table_name):
        file_paths = glob(f'{RESULT_PATH}/*.csv')
        file_names = [os.path.basename(file) for file in file_paths]

        file_name = f'{table_name}.csv'
        if file_name not in file_names:
            return table_name

        sequence = 1
        file_name = f'{table_name}{sequence}.csv'

        while file_name in file_names:
            sequence += 1
            file_name = f'{table_name}{sequence}.csv'

        return f'{table_name}{sequence}'
