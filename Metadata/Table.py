from copy import deepcopy

class Table(object):
    def __init__(self, data):
        self._table_name = data['table_name']
        self._columns = data['columns']
        self._foreign_keys = data['foreign_keys']


    @property
    def table_name(self):
        return deepcopy(self._table_name)


    @table_name.setter
    def table_name(self, value):
        self._table_name = value


    @property
    def columns(self):
        return deepcopy(self._columns)


    def append_column(self, value):
        self._columns.append(value)


    @property
    def foreign_keys(self):
        return deepcopy(self._foreign_keys)


    def append_foreign_keys(self, value):
        self._foreign_keys.append(value)


    def __str__(self):
     return str({
         'table_name': self._table_name,
         'columns': self._columns,
         'foreign_keys': self._foreign_keys
     })
