from abc import abstractmethod

class Case():
    def __init__(self, count, column_metadata):
        self.count = count
        self.column_metadata = column_metadata


    @abstractmethod
    def make_column(self):
        pass