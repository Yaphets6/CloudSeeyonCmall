from src.case_center.case_model import CaseModel
from src.case_center.excel_case_handle import CaseSheet

case_model = CaseModel()
case_model.generate_excel_case_file_model()
case_model.initialization_case_info_table()
case = CaseSheet("F:\\Study\\CloudSeeyonCmall\\src\\case_files\\demo2.xlsx")
content = case.get_all_case_content()
print(content[0])
print(content[1])
