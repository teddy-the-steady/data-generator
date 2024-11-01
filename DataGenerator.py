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

class DataGenerator():
    possible_pair_columns = {}

    def __init__(self, csv):
        self.csv = csv
        self.unsupported_columns = list()


    def make_insert_queries_for_csv(self, count):
        # TODO
        # 1. make sets of each column
        index = Csv.index_of_table(self.csv.tables, 'MST_CUSTOMER')
        for column_metadata in self.csv.tables[index].columns:
            result = self._generate_column_items(count, column_metadata)
            print(column_metadata['column'], result)

        if len(self.unsupported_columns) > 0:
            raise Exception(f'Unsupported columns found: {self.unsupported_columns}')
        #   a. check format (options, code, hankaku, email? and more)
        #   b. consider length + type
        #   c. check constraint (unique=true, pk=true)
        #   d. use random function (+ set)
        # 2. combine list(set) of columns to make rows
        # 3. decide how to deal with FK situation!!!!
        # >> after making up all the columns and then give correction
        # >> when insert, consider the order of tables referring and referred

    def _generate_column_items(self, count, column_metadata):
        column_name = column_metadata['column'].lower()
        column_type = column_metadata['type'].lower()

        if self._has_optional_choice(column_metadata['format']):
            result = Optional(count, column_metadata)
            return result.make_column()

        if self._is_name(column_name):
            result = Name(count, column_metadata)
            return result.make_column()

        if self._is_email(column_name):
            result = Email(count, column_metadata)
            return result.make_column()

        if self._is_address(column_name):
            result = Address(count, column_metadata)
            return result.make_column()

        if self._is_date_or_datetime(column_type):
            result = DateTime(count, column_metadata)
            return result.make_column()

        if self._is_number(column_name, column_type):
            if 'phone_number' in column_name:
                result = PhoneNumber(count, column_metadata)
                return result.make_column()
            else:
                result = Number(count, column_metadata)
                return result.make_column()

        if self._is_code(column_name):
            result = Code(count, column_metadata)
            return result.make_column()

        if Etc.is_etc(column_name):
            result = Etc(count, column_metadata)
            return result.make_column()

        self.unsupported_columns.append(column_metadata['column'])


    def _has_optional_choice(self, column_format):
        return 'C00' in column_format


    def _is_name(self, column_name):
        return 'name' in column_name


    def _is_address(self, column_name):
        return 'address' in column_name


    def _is_email(self, column_name):
        return 'email' in column_name


    def _is_number(self, column_name, column_type):
        ends_with_number = column_name.endswith('number')
        ends_with_no = column_name.endswith('_no')
        type_numeric = column_type.lower() == 'numeric'
        return  ends_with_number or ends_with_no or type_numeric


    def _is_code(self, column_name):
        ends_with_code = column_name.endswith('_code')
        ends_with_id = column_name.endswith('_id')
        return ends_with_code or ends_with_id


    def _is_date_or_datetime(self, column_type):
        return column_type in ['date', 'datetime']
