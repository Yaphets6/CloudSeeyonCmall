import xlrd


class CaseFileHandle:

    def __init__(self, case_path):
        """初始化用例文件"""
        self.case_path = case_path
        self.case_file_obj = self.get_excel_case_file_obj(case_path)

    @staticmethod
    def get_excel_case_file_obj(case_path):
        return xlrd.open_workbook(case_path)

    def get_excel_case_file_all_sheets_name(self):
        sheets_name = self.case_file_obj.sheet_names()
        return sheets_name


class CaseSheetHandle:

    def __init__(self, sheet_name, file_obj):
        self.sheet_name = sheet_name
        self.sheet_obj = self.get_sheet_obj(sheet_name, file_obj)

    @staticmethod
    def get_sheet_obj(sheet_name, file_obj):
        sheets_name = file_obj.get_excel_case_file_all_sheets_name()
        if sheet_name in sheets_name:
            return file_obj.case_file_obj.sheet_by_name(sheet_name)
        else:
            raise Exception("用例文件sheet‘%s’中没有名称为:‘%s’的sheet" % (sheets_name, sheet_name))

    #   根据列头名称，获取该列所有数据（包含列头）
    def get_col_values_by_name(self, name):
        return self.sheet_obj.col_values(self.get_case_col_index_by_name(name))

    #   根据列头名称，获取该列所有数据（不包含列头）
    def get_col_values_not_contains_head(self, name):
        case_col = self.get_col_values_by_name(name)
        del case_col[case_col.index(name)]
        return case_col

    #   获取用例编号列表
    def get_case_number_list(self):
        return self.get_col_values_not_contains_head("用例编号")

    #   获取用例总数
    def get_case_total(self):
        return len(self.get_col_values_not_contains_head("用例编号"))

    #   根据名字找到列序号
    def get_case_col_index_by_name(self, name):
        try:
            case_no_tag_index = self.get_case_key_words().index(name)
            return case_no_tag_index
        except Exception:
            raise Exception("用例sheet中未找到关键字【%s】" % name)

    #   获取列头名称列表
    def get_case_key_words(self):
        if self.sheet_obj:
            return self.sheet_obj.row_values(0)
        else:
            raise Exception("用例sheet对象为空")

    #   获取用例编号所在行的excel内容
    def get_case_content_by_case_number(self, case_number):
        case_index = (self.get_col_values_by_name("用例编号").index(case_number))
        case_key_words = self.get_case_key_words()
        case = self.sheet_obj.row_values(case_index)
        case_content = {}
        for key in case_key_words:
            if key == "执行结果":
                if case[(case_key_words.index(key))] == "":
                    case_content[key] = 0
                else:
                    case_content[key] = case[(case_key_words.index(key))]
            else:
                case_content[key] = case[(case_key_words.index(key))]
        print(case_content)
        return case_content












