import random
from gimei import Gimei
from Cases.Case import Case

class Name(Case):

    @staticmethod
    def is_name(column_name):
        return 'name' in column_name


    def make_column(self):
        if self._is_human_name():
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
        
        if 'taxoffice' in self._get_column_name_lower():
            result = list()
            for i in range(0, self.count):
                result.append(self._get_random_kanji(random.randint(1, 3)) + '税務署')
            return result


    def _get_random_name(self):
        return Gimei().name


    def _is_human_name(self):
        human_name_columns = ['customer_name', 'customer_name_kana', 'delegate_name', 'delegate_name_kana']
        return self._get_column_name_lower() in human_name_columns
