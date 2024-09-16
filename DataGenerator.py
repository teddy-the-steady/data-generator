class DataGenerator():
    def __init__(self, csv):
        self.csv = csv


    def make_insert_queries_for_table(self, table_name):
        if not table_name in self.csv.tables:
            raise Exception('Table name not found')

        print(self.csv.header)
        print(self.csv.tables)
        columns = self.csv.get_columns(table_name)
        # TODO
        # 1. make table a dict
        # {
        #   table_name: 'persons',
        #   columns: [
        #       {column: 'id', type: 'int', constraint: 'pk', length: '', format: ''},
        #       {column: 'name', type: 'varchar(50)', constraint: '', length: 'gte50', format: 'hankaku'},
        #       {column: 'age', type: 'int', constraint: '', length: '', format: 'positive_number'},
        #       {column: 'gender', type: 'char(1)', constraint: '', length: '1', format: 'm/f'},
        #       {column: 'my_number', type: 'char(12)', constraint: 'unique', length: '12', format: 'positive_number'},
        #   ]
        # }
        for column in columns:
            self._column_to_dict(column)
            print('///////////')
        # 2. make sets of each column
        #   a. check constraint (unique=true, pk=true)
        #   b. check format (options, hankaku, email? and more)
        #   c. decide between making a set and using random function
        #   d. make column item (consider length + type)
        # 3. combine sets of column to make rows


    def _column_to_dict(self, column):
        print(column[self.csv.header.index('column')])