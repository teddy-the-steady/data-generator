from abc import abstractmethod
import random
import string

class Case():
    possible_pair_columns = {}

    def __init__(self, count, column_metadata):
        self.count = count
        self.column_metadata = column_metadata


    @abstractmethod
    def make_column(self):
        pass


    def _get_column_name_lower(self):
        return self.column_metadata["column"].lower()


    def _get_random_alpha_numeric_code(self, length):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))


    def _get_random_alphabetic_code(self, length):
       return ''.join(random.choice(string.ascii_letters) for x in range(length))
