import random
from cases.Case import Case

class Year(Case):

    @staticmethod
    def is_year(column_name):
        return 'year' in column_name.lower()


    def make_column(self):
        result = list()
        for i in range(0, self.count):
            result.append(self._get_random_year())

        return result


    def _get_random_year(self):
        return str(random.randrange(1995, 2025))
