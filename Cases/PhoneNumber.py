import random
from Cases.Case import Case

class PhoneNumber(Case):

    @staticmethod
    def is_phone_number(column_name):
        return 'phone_number' in column_name


    def make_column(self):
        result = set()
        while True:
            result.add(self._get_random_phone_number())
            if len(result) == self.count:
                break
        return list(result)
    

    def _get_random_phone_number(self):
        first = random.choice(['070', '080', '090'])
        second = str(random.randint(0, 9999))
        third = str(random.randint(0, 9999))
        return f'{first}-{second.zfill(4)}-{third.zfill(4)}'
    