import random
from pg_data_generator.cases.Case import Case

class Address(Case):
    # Sample addresses for generation
    STREET_NAMES = [
        'Main St', 'Oak Ave', 'Maple Dr', 'Park Blvd', 'Washington St', 'Lake Rd',
        'Hill St', 'Elm St', 'Pine St', 'Cedar Ave', 'River Rd', 'Forest Dr',
        'Sunset Blvd', 'Broadway', 'Market St', 'Church St', 'School St', 'Spring St'
    ]

    CITIES = [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
        'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
        'Seattle', 'Denver', 'Boston', 'Portland', 'Atlanta', 'Miami'
    ]

    STATES = [
        'NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'FL', 'WA', 'CO', 'MA', 'OR', 'GA'
    ]

    @staticmethod
    def is_address(column_name):
        return 'address' in column_name.lower()


    def make_column(self):
        result = list()

        for _ in range(0, self.count):
            result.append(self._get_random_address())

        return list(result)


    def _get_random_address(self):
        street_number = random.randint(1, 9999)
        street_name = random.choice(self.STREET_NAMES)
        city = random.choice(self.CITIES)
        state = random.choice(self.STATES)
        zipcode = random.randint(10000, 99999)
        return f"{street_number} {street_name}, {city}, {state} {zipcode}"