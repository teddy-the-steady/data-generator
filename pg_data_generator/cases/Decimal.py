import re
from pg_data_generator.cases.Case import Case

class Decimal(Case):

    @staticmethod
    def is_decimal(column_type):
        return 'decimal' in column_type.lower()


    def make_column(self):
        result = list()
        try:
            splitted = self._parse_decimal_type(self.column_metadata['type'])
            precision = int(splitted[0])
            scale = int(splitted[1])
        except Exception as e:
            raise ValueError(
                f"Error parsing DECIMAL type for column '{self.column_metadata.get('column', 'unknown')}': "
                f"type='{self.column_metadata['type']}'. {str(e)}"
            )

        for _ in range(0, self.count):
            result.append(self._get_random_number_with_decimal(precision, scale))
        return result


    def _get_random_number_with_decimal(self, precision, scale):
        """
        Generate a random decimal number.

        Args:
            precision: Total number of digits (e.g., 15 for DECIMAL(15,2))
            scale: Number of digits after decimal point (e.g., 2 for DECIMAL(15,2))
        """
        import random

        # Calculate max value based on precision and scale
        # For DECIMAL(15,2): max integer part is 13 digits, max value is 9999999999999.99
        max_integer_digits = precision - scale
        max_value = (10 ** max_integer_digits) - 1

        # Generate random value between 0 and max_value
        integer_part = random.uniform(0, max_value)

        # Round to the specified scale
        result = round(integer_part, scale)

        return str(result)


    def _parse_decimal_type(self, type_str):
        # Strip quotes if present (CSV may quote fields with commas)
        type_str = type_str.strip('"').strip("'")

        # Support comma separator (standard SQL format)
        match = re.search(r'DECIMAL\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', type_str, re.IGNORECASE)
        if match:
            precision = int(match.group(1))
            scale = int(match.group(2))
            return precision, scale
        else:
            raise ValueError(f'Wrong decimal format: {type_str}. Expected DECIMAL(precision,scale)')