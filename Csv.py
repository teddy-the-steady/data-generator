import csv
from Metadata.Table import Table

class Csv():
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.header = self.get_header()
        self.tables = self.get_tables()
        self.foreign_keys = self.get_foreign_keys()


    @staticmethod
    def index_of_table(tables, table_name):
        return [i for i, d in enumerate(tables) if d.table_name == table_name][0]


    def get_header(self):
        with open(self.csv_path, 'r') as file:
            for index, header in enumerate(csv.reader(file)):
                if index == 0:
                    self._check_header(header)

                    self.table_name_index = header.index('table_name')
                    self.column_name_index = header.index('column')
                    self.constraint_index = header.index('constraint')

                    return header


    def get_tables(self):
        result = set()

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if index == 0: continue
                result.add(line[self.table_name_index])

        return list(result)


    def get_foreign_keys(self):
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


    def get_columns(self):
        result = []

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if index == 0: continue
                result.append(line)

        return result


    def csv_to_dict(self):
        tables = []
        for table_name in self.tables:
            table = Table({
                'table_name': table_name,
                'columns': []
            })
            tables.append(table)

        for column in self.get_columns():
            table_name = ''
            dicted_column = dict()
            for header_item in self.header:
                if header_item == 'table_name':
                    table_name = column[self.header.index(header_item)]
                else:
                    dicted_column[header_item] = column[self.header.index(header_item)]

            index = Csv.index_of_table(tables, table_name)
            tables[index].append_column(dicted_column)

        return tables


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
            if not self._get_fk_table(fk_dict) in self.tables:
                raise Exception('Please provide fk table in your csv file.')


    def _get_fk_table(self, fk_dict):
        return fk_dict['constraint'].split('.')[1]