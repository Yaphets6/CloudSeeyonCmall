from src.comm.case_control import LoadingCase
from src.comm.case_function import ApplicationCaseFunction

LoadingCase.save_all_case_content_in_case_table()
cases_number = ["dee_center_001", "dee_center_002", "dee_center_003", "dee_center_004", "dee_center_005",
                "dee_center_006", "v5_index_search_001", "v5_main_001"]
for case_number in cases_number:
    case_function = ApplicationCaseFunction(case_number)
    print(case_function.function_case())
