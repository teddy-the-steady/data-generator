import random
from pg_data_generator.cases.Case import Case

class Int(Case):

    @staticmethod
    def is_int(column_type):
        return column_type.lower() in ['smallint', 'int', 'bigint']


    def make_column(self):
        length_int = int(self.column_metadata['length'] or 1)

        result = list()
        for _ in range(0, self.count):
            result.append(self._get_random_number_lt(length_int))

        return result


    def _get_random_number_lt(self, length):
        return str(random.randrange(1, 10 ** (length)))
