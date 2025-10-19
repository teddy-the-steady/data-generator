from pg_data_generator.cases.Case import Case

class Address(Case):

    @staticmethod
    def is_address(column_name):
        return 'address' in column_name.lower()


    def make_column(self):
        result = list()

        for i in range(0, self.count):
            result.append(self._get_random_address())

        return list(result)


    def _get_random_address(self):
        # TODO] Returning temporary string
        return "One Apple Park Way, Cupertino, CA 95014"