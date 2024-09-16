from Csv import Csv

class DataGenerator():
    def __init__(self, csv):
        self.csv = csv
        self.header = csv.get_header()
        self.tables = csv.get_tables()


    def make_insert_queries_for_table(self):
        print(self.header)
        print(self.tables)
        columns = self.csv.get_columns(self.tables[0])
        print(columns)
