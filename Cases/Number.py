import random
import scipy.stats as stats
from Cases.Case import Case

class Number(Case):

    @staticmethod
    def is_number(column_name, column_type):
        ends_with_number = column_name.endswith('number')
        ends_with_no = column_name.endswith('_no')
        type_numeric = column_type.lower() == 'numeric'
        return  ends_with_number or ends_with_no or type_numeric


    def make_column(self):
        if self._has_decimal():
            result = list()
            splitted = self.column_metadata['length'].split(',')

            for i in range(0, self.count):
                result.append(self._get_random_number_with_decimal(int(splitted[0]), int(splitted[1])))
            return result
        else:
            length_int = int(self.column_metadata['length'])
            is_char = self.column_metadata['type'].lower() == 'char'

            if 'unique' in self.column_metadata['constraint']:
                result = set()
                while True:
                    result.add(
                        self._get_random_number_of_digits(length_int)
                        if is_char else
                        self._get_random_number_lt(length_int)
                    )
                    if len(result) == self.count:
                        break

                return list(result)

            else:
                result = list()
                for i in range(0, self.count):
                    result.append(
                        self._get_random_number_of_digits(length_int)
                        if is_char else
                        self._get_random_number_lt(length_int)
                    )
                return result


    def _get_random_number_lt(self, length):
        return str(random.randrange(1, 10 ** (length)))


    def _get_random_number_of_digits(self, length):
        return str(random.randrange(10 ** (length - 1), 10 ** (length)))


    def _get_random_number_with_decimal(self, length, digits):
        a = 1  # Skewness parameter
        loc = 0  # Location parameter
        scale = 1e9  # Scale parameter (when it comes to money, 1e9 gives billions)

        skewnorm_dist = stats.skewnorm(a, loc, scale)

        num_samples = 1
        random_values = skewnorm_dist.rvs(num_samples)

        filtered_value = [
            round(abs(value), digits) for value in random_values
            if value < 10 ** (length - 1)
        ]

        return str(filtered_value[0])


    def _has_decimal(self):
        return ',' in self.column_metadata['length']