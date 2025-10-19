import random
from cases.Case import Case

class Optional(Case):

    @staticmethod
    def has_optional_choice(column_format):
        return '[' in column_format and ']' in column_format


    def make_column(self):
        result = list()

        options = self.parse_list_string(self.column_metadata['format'])
        for i in range(0, self.count):
            result.append(self._get_random_choice(options))
        return result
    

    def _get_random_choice(self, options_list):
        return str(random.choice(options_list))
    
    
    def parse_list_string(self, stringified_list):
        s = stringified_list.strip()
        if s.startswith('[') and s.endswith(']'):
            s = s[1:-1]
        return s.split(',')
