import os
from glob import glob
import csv
import pandas as pd

from Metadata.Table import Table

RESULT_PATH = 'results' # TODO later change this to Desktop or Download or somewhere else

class Csv():
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.header = self._set_header()
        self.table_names = self._set_table_names()
        self.tables = self._set_tables(self.header, self.table_names)
        self._set_foreign_keys(self.tables)


    @staticmethod
    def index_of_table(tables_dict, table_name):
        index_list = [i for i, d in enumerate(tables_dict) if d.table_name == table_name]
        if len(index_list) == 0:
            raise Exception('Table not found')

        return index_list[0]


    @staticmethod
    def prepare_next_file_name(table_name):
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


    def write_results_to_csv(self, column_name, column_values, file_name):
        file_path = f'{RESULT_PATH}/{file_name}.csv'

        try:
            df = pd.read_csv(file_path, dtype=str)
        except FileNotFoundError:
            with open(file_path, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[column_name])
                writer.writeheader()

            df = pd.DataFrame(columns=[column_name])

        df[column_name] = column_values

        df.to_csv(file_path, index=False)


    def _set_tables(self, header, table_names):
        table_obj_list = self._make_tables_dict(table_names)
        result = self._append_column_metadata(header, table_obj_list)
        return result


    def _make_tables_dict(self, table_names):
        result = []
        for table_name in table_names:
            table = Table({
                'table_name': '',
                'columns': [],
                'foreign_keys': []
            })

            table.table_name = table_name
            result.append(table)

        return result


    def _append_column_metadata(self, header, table_obj_list):
        for column in self._get_columns():
            if column[header.index('constraint')] == 'pk':
                continue

            table_name = ''
            dicted_column = dict()
            for header_item in header:
                if header_item == 'table_name':
                    table_name = column[header.index(header_item)]
                else:
                    dicted_column[header_item] = column[header.index(header_item)]

            index = Csv.index_of_table(table_obj_list, table_name)
            table_obj_list[index].append_column(dicted_column)

        return table_obj_list


    def _get_columns(self):
        result = []

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if index == 0: continue
                result.append(line)

        return result


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


    def _set_foreign_keys(self, tables):
        result = list()

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if 'fk.' in line[self.constraint_index]:
                    result.append({
                        'table_name': line[self.table_name_index],
                        'column': line[self.column_name_index],
                        'constraint': line[self.constraint_index]
                    })

        self._set_fk_to_table(result, tables)


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


    def _set_fk_to_table(self, fk_dicts, tables):
        for fk_dict in fk_dicts:
            if not self._get_fk_target_table(fk_dict) in self.table_names:
                raise Exception('Please provide fk table in your csv file.')

            table = tables[Csv.index_of_table(tables, fk_dict['table_name'])]
            del fk_dict['table_name']
            table.append_foreign_keys(fk_dict)


    def _get_fk_target_table(self, fk_dict):
        return fk_dict['constraint'].split('.')[1]