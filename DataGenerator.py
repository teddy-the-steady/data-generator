import random
from datetime import timedelta, datetime
from gimei import Gimei

class DataGenerator():
    def __init__(self, csv):
        self.csv = csv


    def make_insert_queries_for_table(self, table_name, count):
        if not table_name in self.csv.tables:
            raise Exception('Table name not found')

        columns = self.csv.get_columns(table_name)
        # TODO
        # 1. make table a dict
        columns_dict = self._columns_to_dict(columns)
        # 2. make sets of each column
        for column_dict in columns_dict['columns']:
            print(self._get_random_datetime_between('2024-01-01', '2025-01-01'))
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
    

    def _get_random_choice(self, options_list):
        return random.choice(options_list)
    

    def _get_random_datetime_between(self, start, end):
        try:
            delta = datetime.fromisoformat(end) - datetime.fromisoformat(start)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return datetime.fromisoformat(start) + timedelta(seconds = random_second)


    def _get_random_name(self):
        name = Gimei().name
        return name.kanji
    

    def _get_random_name_kana(self):
        name = Gimei().name
        return name.katakana


    def _get_random_address(self):
        address = Gimei().address
        return address.kanji


    def _get_random_address_kana(self):
        address = Gimei().address
        return address.katakana
    

    def _get_random_code(self, length, type):
        if type == 'number':
            return 1234