from gimei import Gimei
from Cases.Case import Case

class Address(Case):

    @staticmethod
    def is_address(column_name):
        return 'address' in column_name


    def make_column(self):
        if self._has_already_made_up_pairs():
            return self.possible_pair_columns[self._get_column_name_lower()]

        kanji = list()
        kana = list()
        for i in range(0, self.count):
            address = self._get_random_address()
            kanji.append(address.kanji)
            address_kana = address.katakana
            if self._is_hankaku_kana(self.column_metadata['format']):
                address_kana = self._zen_to_han(address_kana)
            kana.append(address_kana)

        return self._set_possible_pair_names_and_return(kanji, kana)


    def _get_random_address(self):
        return Gimei().address