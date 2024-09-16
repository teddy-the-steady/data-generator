class DataGenerator():
    def __init__(self, csv):
        self.csv = csv


    def make_insert_queries_for_table(self, table_name):
        if not table_name in self.csv.tables:
            raise Exception('Table name not found')

        print(self.csv.header)
        print(self.csv.tables)
        columns = self.csv.get_columns(table_name)
        for column in columns:
            insert_values = self.make_insert_values_for_a_column(column)


    def make_insert_values_for_a_column(self, column):
        print(column[self.csv.header.index('column')])
        # TODO
        # 1. make sets of each rows
        # 2. check constraint (unique=true, pk=true)
        # 3. check format (options, hankaku, email? and more)
        # 4. decide between making a set and using random function
        # 5. make row (consider length + type)