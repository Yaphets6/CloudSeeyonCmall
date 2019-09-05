import mysql.connector
from src.comm.case_control import LoadingCase
from src.comm.case_excel_handle import *
from src.comm.case_model import CaseModel
from src.comm.data_base_handle import MysqlBase
from src.comm.case_control import LoadingCase
from src.comm.data_transformation import DataTransformation
from src.confing.application_service_config import *
import requests
from src.comm.application_model import *
from src.comm.case_function import CaseFunction
from src.case_center.case_model import CaseModel
from src.case_center.excel_case_handle import CaseSheet

# file = CaseFileHandle(case_path=LoadingCase.get_all_case_files_path()[0])
# case_sheet = CaseSheetHandle(sheet_name="用户中心", file_obj=file.case_file_obj)
# case_list = case_sheet.get_case_number_list()
# for case in case_list:
#     CaseModel.update_case_by_content(case_sheet.get_case_content_by_case_number(case))
# print(LoadingCase.get_all_case_files_path())

# LoadingCase.save_all_case_content_in_case_table()

# v5_application_session = ApplicationServiceSession(V5).get_v5_session("cs1", "123456")
# s = v5_application_session.get(url="http://seeyonapp.seeyon.com:9999/seeyon/main.do?method=main")
# data = {"managerMethod": "findListDatas", "arguments": [{"pageSize":"20", "pageNo":1,
#         "listType": "1", "spaceType": "", "spaceId": "", "typeId": "", "condition": "title",
#          "textfield1": "1", "textfield2": "", "myNews": ""}]}
#
# data1 = {"accessoryName": "", "author": "", "iframeSearch": "iframeSearch",
#          "keyword": "1","library": 1, "SEARCHDATE_BEGIN": "", "SEARCHDATE_END": "", "searchType": "all", "title": ""}
#
# s2 = v5_application_session.post(url="http://seeyonapp.seeyon.com:9999/seeyon/index/indexController.do?method=searchAll", data=data1)
# s1 = v5_application_session.get(url="http://seeyonapp.seeyon.com:9999/seeyon/collaboration/collaboration.do?method=newColl&rescode=F01_newColl&portalId=-6799825299868071502&_resourceCode=F01_newColl")
# print(s1.text)
# print(s.text)
# print(s2.text)
#
#
# dee_application_session = ApplicationServiceSession(DEE).get_dee_session()
# dee_r_1 = dee_application_session.post(url="http://192.168.225.11:8085/seeyon/rest/dee/task/getCorpInfoByFileNo",
#                                        json={"filesNo":"OLD000019"})
# print(DataTransformation.format_xml_str(dee_r_1.text))

# LoadingCase.save_all_case_content_in_case_table()
# case_list = CaseModel.get_all_case_number()
# print(case_list)

# v5_application = V5Application()
# v5_application.function_v5_application_case()
# chome = CHomeApplication()
# chome.set_c_home_application_token("yangyk", "123456789")
# v5_application = V5Application()
# function = CaseFunction(v5_application)
# function.function_case_by_number("v5_main_001")
# response = requests.get("http://192.168.225.70:80/seeyon/index/indexController.do", params={"method": "searchAll"})
# print(response.url)

case_model = CaseModel()
case_model.generate_excel_case_file_model()
case_model.initialization_case_info_table()
case = CaseSheet("F:\\Study\\CloudSeeyonCmall\\src\\case_files\\demo2.xlsx")
content = case.get_all_case_content()
print(content[0])
print(content[1])
