import random
from pg_data_generator.cases.Case import Case

class Boolean(Case):

    @staticmethod
    def is_boolean(column_type):
        return column_type.lower() in ['boolean', 'bool']


    def make_column(self):
        result = list()
        for _ in range(0, self.count):
            result.append(self._get_random_boolean())

        return result


    def _get_random_boolean(self):
        return str(random.choice(['TRUE', 'FALSE']))
