from gimei import Gimei
from Cases.Case import Case

class HumanName(Case):
    def make_column(self):
        if self._has_already_made_up_pairs():
            return self.possible_pair_columns[self._get_column_name_lower()]

        kanji = list()
        kana = list()
        for i in range(0, self.count):
            name = self._get_random_name()
            kanji.append(name.kanji)
            name_kana = name.katakana
            if self._is_hankaku_kana(self.column_metadata['format']):
                name_kana = self._zen_to_han(name_kana)
            kana.append(name_kana)

        return self._set_possible_pair_names_and_return(kanji, kana)


    def _get_random_name(self):
        return Gimei().name