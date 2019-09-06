from src.case_center.case_model import CaseModel
from src.case_center.excel_case_handle import CaseSheet
from src.comm.project_path import ProjectPath

case_model = CaseModel()
# case_model.generate_excel_case_file_model()
# case_model.initialization_case_info_table()
# case_model.initialization_case_result_table()
# case = CaseSheet("%s\\用例模板1.xlsx" % ProjectPath.case_files_path())
# content = case.get_all_case_content()
# case.dump_case_content_in_case_info_table()
print(case_model.get_case_total_from_case_info())
print(case_model.get_cases_number_list())
case_model.get_case_content_by_case_number("DEE_1")
