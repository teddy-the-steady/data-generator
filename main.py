from Csv import Csv
from DataGenerator import DataGenerator

def openCsv():
    csv = Csv('example.csv')
    dg = DataGenerator(csv)
    dg.make_insert_queries_for_csv(10)
    
openCsv()