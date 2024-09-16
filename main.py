from Csv import Csv


def openCsv():
    csv = Csv('persons.csv')
    title = csv.get_header()
    tables = csv.get_tables()
    columns = csv.get_columns(tables[0])
    
    print(title)
    print(tables)
    print(columns)
    
openCsv()