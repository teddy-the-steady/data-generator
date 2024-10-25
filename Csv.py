import csv
from Metadata.Table import Table

class Csv():
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.header = self._set_header()
        self.table_names = self._set_table_names()
        self.tables = self._set_tables()
        self.foreign_keys = self._set_foreign_keys()


    @staticmethod
    def index_of_table(tables_dict, table_name):
        return [i for i, d in enumerate(tables_dict) if d.table_name == table_name][0]


    def get_columns(self):
        result = []

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if index == 0: continue
                result.append(line)

        return result


    def _set_tables(self):
        table_obj_list = self._make_tables_dict()
        result = self._append_column_metadata(table_obj_list)
        return result


    def _make_tables_dict(self):
        result = []
        for table_name in self.table_names:
            table = Table({
                'table_name': '',
                'columns': [],
                'foreign_keys': []
            })

            table.table_name = table_name
            result.append(table)

        return result


    def _append_column_metadata(self, table_obj_list):
        for column in self.get_columns():
            table_name = ''
            dicted_column = dict()
            for header_item in self.header:
                if header_item == 'table_name':
                    table_name = column[self.header.index(header_item)]
                else:
                    dicted_column[header_item] = column[self.header.index(header_item)]

            index = Csv.index_of_table(table_obj_list, table_name)
            table_obj_list[index].append_column(dicted_column)

        return table_obj_list


    def _set_header(self):
        with open(self.csv_path, 'r') as file:
            for index, header in enumerate(csv.reader(file)):
                if index == 0:
                    self._check_header(header)

                    self.table_name_index = header.index('table_name')
                    self.column_name_index = header.index('column')
                    self.constraint_index = header.index('constraint')

                    return header


    def _set_table_names(self):
        result = set()

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if index == 0: continue
                result.add(line[self.table_name_index])

        return list(result)


    def _set_foreign_keys(self):
        result = list()

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if 'fk.' in line[self.constraint_index]:
                    result.append({
                        'column': f"{line[self.table_name_index]}.{line[self.column_name_index]}",
                        'constraint': line[self.constraint_index]
                    })

        self._check_fk_tables_exist(result)

        return result


    def _check_header(self, header_candidate):
        if not set([
            'table_name',
            'column',
            'type',
            'constraint',
            'length',
            'format'
        ]).issubset(header_candidate):
            raise Exception('No proper header found in csv file')


    def _check_fk_tables_exist(self, fk_dicts):
        for fk_dict in fk_dicts:
            if not self._get_fk_table(fk_dict) in self.table_names:
                raise Exception('Please provide fk table in your csv file.')


    def _get_fk_table(self, fk_dict):
        return fk_dict['constraint'].split('.')[1]