import csv

class Csv():
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.header = self.get_header()
        self.tables = self.get_tables()


    def get_header(self):
        with open(self.csv_path, 'r') as file:
            for index, header in enumerate(csv.reader(file)):
                if index == 0:
                    self._check_header(header)
                    return header


    def get_tables(self):
        tables = set()
        table_name_index = 0

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if index == 0:
                    self._check_header(line)
                    table_name_index = line.index('table_name')
                else:
                    tables.add(line[table_name_index])

        return list(tables)


    def get_columns(self, table_name):
        columns = []
        table_name_index = 0

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if index == 0:
                    self._check_header(line)
                    table_name_index = line.index('table_name')
                elif line[table_name_index] == table_name:
                    columns.append(line)

        return columns


    def _check_header(self, header_candidate):
        if not set(['table_name', 'column', 'type']).issubset(header_candidate):
            raise Exception('No proper header found in csv file')
