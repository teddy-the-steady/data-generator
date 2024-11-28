import random
from cases.Case import Case

class Code(Case):

    @staticmethod
    def is_code(column_name):
        column_name = column_name.lower()
        ends_with_code = column_name.endswith('_code')
        ends_with_id = column_name.endswith('_id')
        return ends_with_code or ends_with_id


    def make_column(self):
        if self._is_post_code():
            result = set()
            while True:
                result.add(self.get_random_post_code())
                if len(result) == self.count:
                    break
            return list(result)

        else:
            if self._is_id():
                length_int = int(self.column_metadata['length'])

                result = list()
                value = self._get_code_starting_from_digit_numbers_of_ten(length_int)
                for i in range(0, self.count):
                    result.append(str(value))
                    value += 1
                return result

            if self._is_code():
                length_int = int(self.column_metadata['length'])

                result = list()
                value = 1
                for i in range(0, self.count):
                    result.append(str(value).zfill(length_int))
                    value += 1
                return result


    def _get_code_starting_from_digit_numbers_of_ten(self, length):
        return 10 ** (length - 1)


    def get_random_post_code(self):
        first = str(random.randint(100, 999))
        second = str(random.randint(0, 9999))
        return f'{first}-{second.zfill(4)}'


    def _is_post_code(self):
        return 'post_code' in self._get_column_name_lower()


    def _is_code(self):
        return self._get_column_name_lower().endswith('_code')


    def _is_id(self):
        return self._get_column_name_lower().endswith('_id')