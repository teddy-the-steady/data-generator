import random
from Database import Database
from Cases.Case import Case

class Optional(Case):
    def make_column(self):
        result = list()

        # TODO] temp comment for no database setup case
        # db = Database()
        # options = db._select_options(self.column_metadata['format'])
        options = [0, 1, 2]
        for i in range(0, self.count):
            result.append(self._get_random_choice(options))
        return result
    

    def _get_random_choice(self, options_list):
        return random.choice(options_list)
    