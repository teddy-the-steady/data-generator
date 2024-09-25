from Csv import Csv
from DataGenerator import DataGenerator
from Database import Database


def openCsv():
    csv = Csv('MST_CUSTOMER.csv')
    dg = DataGenerator(csv)
    dg.make_insert_queries_for_table('MST_CUSTOMER', 10)
    
openCsv()