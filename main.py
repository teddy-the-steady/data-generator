from Csv import Csv
from DataGenerator import DataGenerator

def run():
    csv = Csv('example.csv')
    dg = DataGenerator(csv)
    dg.make_insert_queries_for_tables(10000)
    
run()