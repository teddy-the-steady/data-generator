import csv

class Csv():
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.header = self.get_header()
        self.tables = self.get_tables()
        self.foreign_keys = self.get_foreign_keys()


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
                if index == 0:
                    self._check_header(line)
                else:
                    result.add(line[self.table_name_index])

        return list(result)


    def get_foreign_keys(self):
        result = list()

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if index == 0:
                    self._check_header(line)
                else:
                    if 'fk.' in line[self.constraint_index]:
                        result.append({
                            'column': f"{line[self.table_name_index]}.{line[self.column_name_index]}",
                            'constraint': line[self.constraint_index]
                        })

        return result


    def get_columns(self, table_name):
        result = []
        table_name_index = 0

        with open(self.csv_path, 'r') as file:
            for index, line in enumerate(csv.reader(file)):
                if index == 0:
                    self._check_header(line)
                    table_name_index = line.index('table_name')
                elif line[table_name_index] == table_name:
                    result.append(line)

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
