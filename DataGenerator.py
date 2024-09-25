import random
import string
from datetime import timedelta, datetime
from gimei import Gimei
import mojimoji
from Database import Database


class DataGenerator():
    column = {}
    possible_pair_columns = {}

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
        print(columns_dict)
        for column_dict in columns_dict['columns']:
            self.column = column_dict
            result = self._generate_column_items(10)
            print(result)
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
        result = list()
        if self._has_optional_choice():
            db = Database()
            options = db._select_options(self.column['format'])
            for i in range(1, count):
                result.append(self._get_random_choice(options))
            return result

        if self._is_name():
            column_name_lower = self.column['column'].lower()

            if self._is_human_name(column_name_lower):
                if self._has_already_made_up_name_pairs(column_name_lower):
                    return self.possible_pair_columns[column_name_lower]

                kanji = list()
                kana = list()
                for i in range(1, count):
                    name = self._get_random_name()
                    kanji.append(name.kanji)
                    name_kana = name.katakana
                    if self._is_hankaku_kana:
                        name_kana = self._zen_to_han(name_kana)
                    kana.append(name_kana)

                return self._set_possible_pair_columns_and_return(column_name_lower, kanji, kana)


    def _has_optional_choice(self):
        return 'C00' in self.column['format']


    def _is_name(self):
        return 'name' in self.column['column'].lower()


    def _is_human_name(self, column_name_lower):
        human_name_columns = ['customer_name', 'customer_name_kana']
        return column_name_lower in human_name_columns


    def _has_already_made_up_name_pairs(self, column_name_lower):
        return column_name_lower in self.possible_pair_columns.keys()


    def _set_possible_pair_columns_and_return(self, column_name_lower, kanji, kana):
        if 'kana' in column_name_lower:
            self.possible_pair_columns[column_name_lower.replace('kana', '')] = kanji
            self.possible_pair_columns[column_name_lower] = kana

            return self.possible_pair_columns[column_name_lower]
        else:
            self.possible_pair_columns[column_name_lower] = kanji
            self.possible_pair_columns[column_name_lower + 'kana'] = kana

            return self.possible_pair_columns[column_name_lower]


    def _is_hankaku_kana(self):
        return 'hankaku_kana' in self.column['format']


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
        return Gimei().name


    def _zen_to_han(self, str):
        return mojimoji.zen_to_han(str)


    def _get_random_address(self):
        return Gimei().address


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
