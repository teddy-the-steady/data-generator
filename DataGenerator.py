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
            result = self._generate_column_items(count)
            print(self.column['column'], result)
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
        result = set()
        column_name_lower = self.column['column'].lower()

        if self._has_optional_choice(self.column['format']):
            db = Database()
            options = db._select_options(self.column['format'])
            options_result = list()
            for i in range(0, count):
                options_result.append(self._get_random_choice(options))
            return options_result

        if self._is_name(column_name_lower):
            if self._is_human_name(column_name_lower):
                if self._has_already_made_up_pairs(column_name_lower):
                    return self.possible_pair_columns[column_name_lower]

                kanji = list()
                kana = list()
                for i in range(0, count):
                    name = self._get_random_name()
                    kanji.append(name.kanji)
                    name_kana = name.katakana
                    if self._is_hankaku_kana(self.column['format']):
                        name_kana = self._zen_to_han(name_kana)
                    kana.append(name_kana)

                return self._set_possible_pair_names_and_return(column_name_lower, kanji, kana)

        if self._is_address(column_name_lower):
            if self._has_already_made_up_pairs(column_name_lower):
                return self.possible_pair_columns[column_name_lower]

            kanji = list()
            kana = list()
            for i in range(0, count):
                address = self._get_random_address()
                kanji.append(address.kanji)
                address_kana = address.katakana
                if self._is_hankaku_kana(self.column['format']):
                    name_kana = self._zen_to_han(address_kana)
                kana.append(address_kana)

            return self._set_possible_pair_names_and_return(column_name_lower, kanji, kana)

        if self._is_date_or_datetime():
            if 'datetime' in self.column['type'].lower():
                while True:
                    result.add(self._get_random_datetime_between('2024-01-01', '2024-05-10'))
                    if len(result) == count:
                        break
                return list(result)
            if 'date' in self.column['type'].lower():
                if self._is_date_pair(column_name_lower):
                    if self._has_already_made_up_pairs(column_name_lower):
                        return self.possible_pair_columns[column_name_lower]

                    start_date = set()
                    while True:
                        start_date.add(self._get_random_datetime_between('2018-01-01', '2023-12-31', is_date_only=True))
                        if len(start_date) == count:
                            break

                    end_date = set()
                    while True:
                        end_date.add(self._get_random_datetime_between('2024-01-01', '2024-05-10', is_date_only=True))
                        if len(end_date) == count:
                            break

                    return self._set_possible_pair_dates_and_return(column_name_lower, list(start_date), list(end_date))

                while True:
                    result.add(self._get_random_datetime_between('2024-01-10', '2024-05-10', is_date_only=True))
                    if len(result) == count:
                        break
                return result

        if self._is_number(column_name_lower):
            if 'phone_number' in column_name_lower:
                return self._get_random_phone_number()


    def _has_optional_choice(self, column_format):
        return 'C00' in column_format


    def _is_name(self, column_name_lower):
        return 'name' in column_name_lower


    def _is_address(self, column_name_lower):
        return 'address' in column_name_lower


    def _is_number(self, column_name_lower):
        return column_name_lower.endswith('number')


    def _is_date_or_datetime(self):
        return self.column['type'].lower() in ['date', 'datetime']


    def _is_date_pair(self, column_name_lower):
        return any(x in column_name_lower for x in ['start', 'end'])


    def _is_human_name(self, column_name_lower):
        human_name_columns = ['customer_name', 'customer_name_kana', 'delegate_name', 'delegate_name_kana']
        return column_name_lower in human_name_columns


    def _has_already_made_up_pairs(self, column_name_lower):
        return column_name_lower in self.possible_pair_columns.keys()


    def _set_possible_pair_names_and_return(self, column_name_lower, kanji, kana):
        if 'kana' in column_name_lower:
            self.possible_pair_columns[column_name_lower.replace('kana', '')] = kanji
            self.possible_pair_columns[column_name_lower] = kana

            return self.possible_pair_columns[column_name_lower]
        else:
            self.possible_pair_columns[column_name_lower] = kanji
            self.possible_pair_columns[column_name_lower + 'kana'] = kana

            return self.possible_pair_columns[column_name_lower]


    def _set_possible_pair_dates_and_return(self, column_name_lower, start_date, end_date):
        if 'start' in column_name_lower:
            self.possible_pair_columns[column_name_lower] = start_date
            self.possible_pair_columns[column_name_lower.replace('start', 'end')] = end_date

            return self.possible_pair_columns[column_name_lower]
        elif 'end' in column_name_lower:
            self.possible_pair_columns[column_name_lower] = end_date
            self.possible_pair_columns[column_name_lower.replace('end', 'start')] = start_date

            return self.possible_pair_columns[column_name_lower]


    def _is_hankaku_kana(self, column_format):
        return 'hankaku_kana' in column_format


    def _get_random_choice(self, options_list):
        return random.choice(options_list)


    def _get_random_datetime_between(self, start, end, is_date_only=False):
        try:
            delta = datetime.fromisoformat(end) - datetime.fromisoformat(start)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)

        result = datetime.fromisoformat(start) + timedelta(seconds = random_second)
        if is_date_only:
            return str(result).split()[0]
        return result.__str__()


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


    def _get_random_phone_number(self):
        first = random.choice(['070', '080', '090'])
        second = str(random.randint(0, 9999))
        third = str(random.randint(0, 9999))
        return f'{first}-{second.zfill(4)}-{third.zfill(4)}'