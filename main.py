from Csv import Csv


def openCsv():
    csv = Csv('persons.csv')
    title = csv.get_title()
    tables = csv.get_tables()
    columns = csv.get_columns('persons')
    
    print(title)
    print(tables)
    print(columns)
    
openCsv()