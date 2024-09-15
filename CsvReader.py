import csv

class CsvReader():
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def get_csv_reader(self):
        self.file = open(self.csv_path, 'r')
        reader = csv.reader(self.file)
        return reader

    def close(self):
        self.file.close()