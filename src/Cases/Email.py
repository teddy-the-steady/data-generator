from Cases.Case import Case
import json
import random

class Email(Case):

    @staticmethod
    def is_email(column_name):
        return 'email' in column_name


    def make_column(self):
        with open('Cases/username.json', 'r') as file:
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