class Table(object):
    def __init__(self, data):
        self._table_name = data['table_name']
        self._columns = data['columns']


    @property
    def table_name(self):
        return self._table_name


    @table_name.setter
    def table_name(self, value):
        self._table_name = value


    @property
    def columns(self):
        return self._columns


    def append_column(self, value):
        self._columns.append(value)


    @staticmethod
    def index_of_table(tables, table_name):
        return [i for i, d in enumerate(tables) if d.table_name == table_name][0]


    def __str__(self):
     return str({
         'table_name': self._table_name,
         'columns': self._columns
     })
