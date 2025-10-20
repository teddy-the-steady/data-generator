import re
import scipy.stats as stats
from pg_data_generator.cases.Case import Case

class Decimal(Case):

    @staticmethod
    def is_decimal(column_type):
        return 'decimal' in column_type.lower()


    def make_column(self):
        result = list()
        splitted = self._parse_decimal_type(self.column_metadata['type'])

        for _ in range(0, self.count):
            result.append(self._get_random_number_with_decimal(int(splitted[0]), int(splitted[1])))
        return result


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


    def _parse_decimal_type(self, type_str):
        match = re.search(r'DECIMAL\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', type_str, re.IGNORECASE)
        if match:
            precision = int(match.group(1))
            scale = int(match.group(2))
            return precision, scale
        else:
            raise ValueError('Wrong decimal format')