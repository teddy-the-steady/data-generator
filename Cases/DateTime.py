from Cases.Case import Case
import random
from datetime import timedelta, datetime

class DateTime(Case):
    def make_column(self):
        result = set()
        if self._is_datetime():
            while True:
                result.add(self._get_random_datetime_between('2024-01-01', '2024-05-10'))
                if len(result) == self.count:
                    break
            return list(result)

        if self._is_date():
            if self._is_date_pair(self._get_column_name_lower()):
                if self._has_already_made_up_pairs():
                    return self.possible_pair_columns[self._get_column_name_lower()]

                start_date = set()
                while True:
                    start_date.add(self._get_random_datetime_between('2018-01-01', '2023-12-31', is_date_only=True))
                    if len(start_date) == self.count:
                        break

                end_date = set()
                while True:
                    end_date.add(self._get_random_datetime_between('2024-01-01', '2024-05-10', is_date_only=True))
                    if len(end_date) == self.count:
                        break

                return self._set_possible_pair_dates_and_return(list(start_date), list(end_date))

            while True:
                result.add(self._get_random_datetime_between('2024-01-10', '2024-05-10', is_date_only=True))
                if len(result) == self.count:
                    break

            return list(result)


    def _is_datetime(self):
        return 'datetime' in self.column_metadata['type'].lower()


    def _is_date(self):
        return 'date' in self.column_metadata['type'].lower()


    def _is_date_pair(self, column_name_lower):
        return any(x in column_name_lower for x in ['start', 'end'])


    def _get_random_datetime_between(self, start, end, is_date_only=False):
        try:
            delta = datetime.fromisoformat(end) - datetime.fromisoformat(start)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)

        result = datetime.fromisoformat(start) + timedelta(seconds = random_second)
        if is_date_only:
            return str(result).split()[0]
        return result.__str__()


    def _set_possible_pair_dates_and_return(self, start_date, end_date):
        if 'start' in self._get_column_name_lower():
            self.possible_pair_columns[self._get_column_name_lower()] = start_date
            self.possible_pair_columns[self._get_column_name_lower().replace('start', 'end')] = end_date

            return self.possible_pair_columns[self._get_column_name_lower()]
        elif 'end' in self._get_column_name_lower():
            self.possible_pair_columns[self._get_column_name_lower()] = end_date
            self.possible_pair_columns[self._get_column_name_lower().replace('end', 'start')] = start_date

            return self.possible_pair_columns[self._get_column_name_lower()]