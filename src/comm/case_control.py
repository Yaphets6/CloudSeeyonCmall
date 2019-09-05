from src.comm.case_excel_handle import *
import os
from src.comm.case_model import CaseModel
import datetime
import time


class LoadingCase:

    @staticmethod
    #   获取工程下用例文件的绝对路径
    def get_case_path():
        current_path = os.getcwd()
        case_files_path = current_path[:current_path.index("src") + len("src\\")] + "case_files\\"
        return case_files_path

    @staticmethod
    def get_all_case_files_name():
        return os.listdir(LoadingCase.get_case_path())

    @staticmethod
    def get_all_case_files_path():
        case_path = []
        case_files_path = LoadingCase.get_case_path()
        files_name = LoadingCase.get_all_case_files_name()
        for file_name in files_name:
            case = case_files_path + file_name
            print(case)
            case_path.append(case)
        return case_path

    @staticmethod
    def save_case_content_in_case_table(case_file_path, case_sheet_name):
        file_obj = CaseFileHandle(case_file_path)
        sheet_obj = CaseSheetHandle(case_sheet_name, file_obj)
        case_number_list = sheet_obj.get_case_number_list()
        for case_number in case_number_list:
            CaseModel.update_case_by_content(sheet_obj.get_case_content_by_case_number(case_number))

    @staticmethod
    def save_case_content_by_case_file_path(case_file_path):
        file_obj = CaseFileHandle(case_file_path)
        sheets_name = file_obj.get_excel_case_file_all_sheets_name()
        for sheet_name in sheets_name:
            if "维护" not in sheet_name:
                sheet_obj = CaseSheetHandle(sheet_name, file_obj)
                case_number_list = sheet_obj.get_case_number_list()
                print("将更新<%s>中的<%s>条用例" % (sheet_name, len(case_number_list)))
                start_time = time.time()
                for case_number in case_number_list:
                    CaseModel.update_case_by_content(sheet_obj.get_case_content_by_case_number(case_number))
                end_time = time.time()
                times = end_time - start_time
                print("更新<%s>条用例耗时<%.2f>秒" % (len(case_number_list),times))
                print("<%s>用例更新完成" % sheet_name)
            else:
                print("维护数据不做更新")

    @staticmethod
    def save_all_case_content_in_case_table():
        files_path = LoadingCase.get_all_case_files_path()
        CaseModel.initialization_case_base_table()
        for file_path in files_path:
            print("即将更新用例文件<%s>" % file_path)
            LoadingCase.save_case_content_by_case_file_path(file_path)
