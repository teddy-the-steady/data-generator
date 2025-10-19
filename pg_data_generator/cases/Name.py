import random
from pg_data_generator.cases.Case import Case

class Name(Case):

    @staticmethod
    def is_name(column_name):
        return 'name' in column_name.lower()


    def make_column(self):
        if self._is_human_name():
            result = list()
            for i in range(0, self.count):
                result.append(self._get_random_name())

            return result


    def _get_random_name(self):
        # TODO] Returning temporary string
        return 'Taeho Jeon'


    def _is_human_name(self):
        human_name_columns = ['customer_name', 'given_name', 'family_name', 'first_name', 'last_name']
        return self._get_column_name_lower() in human_name_columns
