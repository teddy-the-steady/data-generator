import random
import scipy.stats as stats
from Cases.Case import Case


class Number(Case):
    def make_column(self):
        if self._has_decimal():
            result = list()
            splitted = self.column_metadata['length'].split(',')

            for i in range(0, self.count):
                result.append(self._get_random_number_with_decimal(int(splitted[0]), int(splitted[1])))
            return result

        return self._get_random_number_code(3)


    def _get_random_number_code(self, length):
        return random.randrange(10 ** (length - 1), 10 ** (length))


    def _get_random_number_with_decimal(self, length, digits):
        a = 1  # Skewness parameter
        loc = 0  # Location parameter (mean)
        scale = 1e11  # Scale parameter (standard deviation)

        skewnorm_dist = stats.skewnorm(a, loc, scale)

        num_samples = 1
        random_values = skewnorm_dist.rvs(num_samples)

        filtered_values = [
            round(value, 2) for value in random_values 
            if value >= 0 and value < 1e12
        ]

        return filtered_values[:10]


    def _has_decimal(self):
        return ',' in self.column_metadata['length']