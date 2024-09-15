from DataGenerator import DataGenerator
import csv


def openCsv():
    dg = DataGenerator('persons.csv')
    reader = dg.get_csv_reader()
    
    for line in reader:
        print(line)
    
    dg.close()

openCsv()