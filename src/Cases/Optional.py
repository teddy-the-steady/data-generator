import random
from cases.Case import Case

class Optional(Case):

    @staticmethod
    def has_optional_choice(column_format):
        return '[' in column_format and ']' in column_format


    def make_column(self):
        result = list()

        options = eval(self.column_metadata['format'])
        for i in range(0, self.count):
            result.append(self._get_random_choice(options))
        return result
    

    def _get_random_choice(self, options_list):
        return str(random.choice(options_list))
    