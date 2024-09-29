import random
from Database import Database
from Case import Case


class Optional(Case):
    result = list()

    def make_column(self):
        db = Database()
        options = db._select_options(self.column_metadata['format'])
        for i in range(0, self.count):
            self.result.append(self._get_random_choice(options))
        return self.result
    

    def _get_random_choice(self, options_list):
        return random.choice(options_list)
    