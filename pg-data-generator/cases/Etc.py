from cases.Case import Case

class Etc(Case):

    @staticmethod
    def is_etc(column_name):
        etc_list = ['comment', 'row_version']
        return column_name.lower() in etc_list


    def make_column(self):
        result = list()
        for i in range(0, self.count):
            result.append('')
        return result
