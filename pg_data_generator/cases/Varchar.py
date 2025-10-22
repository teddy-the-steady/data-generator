import random
import string
from pg_data_generator.cases.Case import Case

class Varchar(Case):
    """
    Handler for generic VARCHAR and CHAR text columns that don't match
    any specific pattern (name, email, address, code, etc.).

    Generates random alphanumeric strings up to the specified length.
    """

    @staticmethod
    def is_varchar(column_type):
        """Check if column is VARCHAR or CHAR type."""
        column_type_lower = column_type.lower()
        return any(t in column_type_lower for t in ['varchar', 'char', 'text'])

    def make_column(self):
        """Generate random text strings for VARCHAR/CHAR columns."""
        length = int(self.column_metadata.get('length') or 10)

        result = []
        for _ in range(0, self.count):
            result.append(self._generate_random_text(length))

        return result

    def _generate_random_text(self, max_length):
        """
        Generate random alphanumeric text.

        Creates varied length strings (50-100% of max_length) with
        mixed case letters, numbers, and spaces.
        """
        # Vary the actual length (50-100% of max length)
        actual_length = random.randint(max(1, max_length // 2), max(1, max_length))

        # Generate random words separated by spaces
        words = []
        remaining_length = actual_length

        while remaining_length > 0:
            # Word length between 3-8 characters
            word_len = min(random.randint(3, 8), remaining_length)

            # Generate random word with mixed case
            word = ''.join(random.choices(string.ascii_letters, k=word_len))
            words.append(word)

            remaining_length -= word_len

            # Add space between words if there's room
            if remaining_length > 0:
                words.append(' ')
                remaining_length -= 1

        result = ''.join(words)[:actual_length]
        return result
