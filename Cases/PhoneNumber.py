import random
from Database import Database
from Cases.Case import Case


class PhoneNumber(Case):
    result = list()

    def make_column(self):
        return self._get_random_phone_number()
    

    def _get_random_phone_number(self):
        first = random.choice(['070', '080', '090'])
        second = str(random.randint(0, 9999))
        third = str(random.randint(0, 9999))
        return f'{first}-{second.zfill(4)}-{third.zfill(4)}'
    