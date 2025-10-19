from pg_data_generator.core.Csv import Csv
from pg_data_generator.core.DataGenerator import DataGenerator

def run():
    csv = Csv('../example.csv')
    dg = DataGenerator(csv)
    dg.make_csv_for_tables(10)
