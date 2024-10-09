import random
from Cases.Case import Case

class Code(Case):
    def make_column(self):
        if self._is_post_code():
            result = set()
            while True:
                result.add(self.get_random_post_code())
                if len(result) == self.count:
                    break
            return list(result)


    def get_random_post_code(self):
        first = str(random.randint(100, 999))
        second = str(random.randint(0, 9999))
        return f'{first}-{second.zfill(4)}'


    def _is_post_code(self):
        return 'post_code' in self._get_column_name_lower()