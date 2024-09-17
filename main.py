from Csv import Csv
from DataGenerator import DataGenerator


def openCsv():
    csv = Csv('persons.csv')
    dg = DataGenerator(csv)
    dg.make_insert_queries_for_table('persons', 1000)
    
openCsv()