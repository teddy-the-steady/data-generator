from Csv import Csv


def openCsv():
    csv = Csv('persons.csv')
    title = csv.get_title()
    tables = csv.get_tables()
    
    print(title)
    print(tables)
    
openCsv()