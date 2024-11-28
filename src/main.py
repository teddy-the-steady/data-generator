from Csv import Csv
from DataGenerator import DataGenerator

def run():
    csv = Csv('../example.csv')
    dg = DataGenerator(csv)
    dg.make_csv_for_tables(10)
    
run()