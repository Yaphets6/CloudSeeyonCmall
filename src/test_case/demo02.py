import unittest
from src.comm.case_excel_handle import *
from src.comm.data_transformation import *
import logging

class demo02(unittest.TestCase):

    def test_case02(self):
        case_file = CaseFileHandle(case_path="F:\接口\接口Demo1.xlsx")
        case_sheet = CaseSheetHandle()
        case_sheet.__get_sheet_obj_by_name__(sheet_name="用户中心")
        cases = case_sheet.get_all_case_number()

        print(cases)
        # for case_number in cases:
        case = Case()
        case_response_obj = case.function_case_by_case_number(cases[0])

        # case_number = "uc_center_001"
        # print(sheet.get_all_case_number())
        # print(sheet.get_all_case_total())
        # print(sheet.get_case_key_words())
        # print(sheet.get_case_content_by_case_number(case_number))
        # case = Case(sheet, case_number)
        # print(case.get_request_url_by_case_number())
        # print(case.get_case_method())
        # function_case = case.function_case()
        # print(function_case)
        # print(case.assert_function_case_check_list(function_case))
        # response_xml = case.get_function_case_response_json(function_case)vv

        # response_json = response_data.change_response_xml_to_json(response_xml)
        # dict_handle = DictHandle()
        # print(response_json)
        # except_value = case.get_case_except_value()
        # print(except_value)
        # print(type(except_value))
        #
        # print(dict_handle.get_value_by_key("orgid", response_json))


