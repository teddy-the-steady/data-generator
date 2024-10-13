from Csv import Csv
from DataGenerator import DataGenerator

def openCsv():
    csv = Csv('MST_CUSTOMER.csv')
    dg = DataGenerator(csv)
    dg.make_insert_queries_for_table('MST_CUSTOMER', 10)
    
openCsv()