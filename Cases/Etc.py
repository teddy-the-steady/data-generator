from Cases.Case import Case

class Etc(Case):
    @staticmethod
    def is_etc(column_name_lower):
        etc_list = ['business_content', 'comment', 'general_purpose_item_1', 'general_purpose_item_2', 'general_purpose_item_3', 'row_version']
        return column_name_lower in etc_list


    def make_column(self):
        result = list()
        for i in range(0, self.count):
            result.append(123)
        return result
