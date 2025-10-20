from pg_data_generator.cases.Case import Case
import json
import random

class Email(Case):

    @staticmethod
    def is_email(column_name):
        return 'email' in column_name.lower()


    def make_column(self):
        import os
        # Get path relative to this file's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        username_file = os.path.join(current_dir, 'username.json')

        with open(username_file, 'r') as file:
            data = json.load(file)
        
            result = set()
            while True:
                index = random.randrange(0, len(data['usernames']))
                result.add(self._make_random_gmail(data['usernames'][index]))
                if len(result) == self.count:
                    break

            return list(result)


    def _make_random_gmail(self, username):
        return f'{username}{random.randrange(1, 999)}@gmail.com'