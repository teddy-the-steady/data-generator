import random
import string
from datetime import timedelta, datetime

from Cases.Optional import Optional
from Cases.HumanName import HumanName
from Cases.Address import Address
from Cases.PhoneNumber import PhoneNumber
from Cases.DateTime import DateTime



class DataGenerator():
    possible_pair_columns = {}

    def __init__(self, csv):
        self.csv = csv


    def make_insert_queries_for_table(self, table_name, count):
        if not table_name in self.csv.tables:
            raise Exception('Table name not found')

        columns = self.csv.get_columns(table_name)
        # TODO
        # 1. make table a dict
        columns_metadata = self._columns_to_dict(columns)
        # 2. make sets of each column
        print(columns_metadata)
        for column_metadata in columns_metadata['columns']:
            self.column_metadata = column_metadata
            result = self._generate_column_items(count)
            print(self.column_metadata['column'], result)
        #   a. check format (options, code, hankaku, email? and more)
        #   b. consider length + type
        #   c. check constraint (unique=true, pk=true)
        #   d. use random function (+ set)
        # 3. combine list(set) of columns to make rows


    def _columns_to_dict(self, columns):
        dicted_columns = []
        for column in columns:
            dicted_column = dict()
            for header_item in self.csv.header:
                if not header_item == 'table_name':
                    dicted_column[header_item] = column[self.csv.header.index(header_item)]
            dicted_columns.append(dicted_column)

        return {
            'table_name': columns[0][self.csv.header.index('table_name')],
            'columns': dicted_columns
        }


    def _generate_column_items(self, count):
        column_name_lower = self.column_metadata['column'].lower()

        if self._has_optional_choice(self.column_metadata['format']):
            result_temp = Optional(count, self.column_metadata)
            return result_temp.make_column()

        if self._is_name(column_name_lower):
            if self._is_human_name(column_name_lower):
                result_temp = HumanName(count, self.column_metadata)
                return result_temp.make_column()

        if self._is_address(column_name_lower):
            result_temp = Address(count, self.column_metadata)
            return result_temp.make_column()

        if self._is_date_or_datetime():
            result_temp = DateTime(count, self.column_metadata)
            return result_temp.make_column()

        if self._is_number(column_name_lower):
            if 'phone_number' in column_name_lower:
                result_temp = PhoneNumber(count, self.column_metadata)
                return result_temp.make_column()


    def _has_optional_choice(self, column_format):
        return 'C00' in column_format


    def _is_name(self, column_name_lower):
        return 'name' in column_name_lower


    def _is_address(self, column_name_lower):
        return 'address' in column_name_lower


    def _is_number(self, column_name_lower):
        return column_name_lower.endswith('number')


    def _is_date_or_datetime(self):
        return self.column_metadata['type'].lower() in ['date', 'datetime']


    def _is_human_name(self, column_name_lower):
        human_name_columns = ['customer_name', 'customer_name_kana', 'delegate_name', 'delegate_name_kana']
        return column_name_lower in human_name_columns


    def _get_random_number_code(self, length):
        return random.randrange(10 ** (length - 1), 10 ** (length))


    def _get_random_alpha_numeric_code(self, length):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))


    def _get_random_alphabetic_code(self, length):
       return ''.join(random.choice(string.ascii_letters) for x in range(length))


    def _get_random_hiragana(self, length):
        result = ''
        for i in range(1, length + 1):
            result += chr(random.randrange(0x3041, 0x309B))
        return result


    def _get_random_katakana(self, length):
        result = ''
        for i in range(1, length + 1):
            result += chr(random.randrange(0x30a1, 0x30F7))
        return result


    def _get_random_kanji(self, length):
        result = ''
        for i in range(1, length + 1):
            result += chr(random.randrange(0x4e00, 0x9fa1))
        return result