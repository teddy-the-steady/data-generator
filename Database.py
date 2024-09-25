import pyodbc


class Database():
    def __init__(self):
        DRIVER= '{ODBC Driver 17 for SQL Server}'
        SERVER = 'localhost'
        DATABASE = 'trustsol'

        connectionString = f'''
                            DRIVER={DRIVER};
                            SERVER={SERVER};
                            DATABASE={DATABASE};
                            Trusted_connection=yes;
                            '''
        
        self.conn = pyodbc.connect(connectionString)
        self.cursor = self.conn.cursor()


    def __del__(self):
        self.conn.close()


    def fetch_all(self,query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows


    def commit(self):
        self.conn.commit()


    def _select_options(self, division_code):
        result = self.fetch_all(f'''
            select ITEM_CODE from MST_CODE
            where DIVISION_CODE = '{division_code}'
        ''')

        def from_tuple_list_to_list(original_list):
            return [item[0] for item in original_list]

        return from_tuple_list_to_list(result)