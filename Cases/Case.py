from abc import abstractmethod
import mojimoji

class Case():
    possible_pair_columns = {}

    def __init__(self, count, column_metadata):
        self.count = count
        self.column_metadata = column_metadata


    @abstractmethod
    def make_column(self):
        pass


    def _get_column_name_lower(self):
        return self.column_metadata["column"].lower()


    def _is_hankaku_kana(self, column_format):
        return 'hankaku_kana' in column_format


    def _zen_to_han(self, str):
        return mojimoji.zen_to_han(str)


    def _has_already_made_up_pairs(self):
        return self._get_column_name_lower() in self.possible_pair_columns.keys()


    def _set_possible_pair_names_and_return(self, kanji, kana):
        if 'kana' in self._get_column_name_lower():
            self.possible_pair_columns[self._get_column_name_lower().replace('kana', '')] = kanji
            self.possible_pair_columns[self._get_column_name_lower()] = kana

            return self.possible_pair_columns[self._get_column_name_lower()]
        else:
            self.possible_pair_columns[self._get_column_name_lower()] = kanji
            self.possible_pair_columns[self._get_column_name_lower() + 'kana'] = kana

            return self.possible_pair_columns[self._get_column_name_lower()]