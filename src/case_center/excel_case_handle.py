import xlrd
from src.case_center.case_model import CaseModel


class ExcelCase(CaseModel):
	
	def __init__(self, excel_case_file_path):
		self.excel_case = xlrd.open_workbook(excel_case_file_path)
		CaseModel.__init__(self)
		
	def get_all_sheets_name(self):
		return self.excel_case.sheet_names()


class CaseSheet(ExcelCase):
	
	def __init__(self, excel_case_file_path):
		ExcelCase.__init__(self, excel_case_file_path)
		
	def get_case_sheets_name(self):
		case_sheets_name = []
		for name in self.get_all_sheets_name():
			try:
				sheet_head = self.excel_case.sheet_by_name(name).row_values(0)
				if sheet_head == self.case_keywords:
					case_sheets_name.append(name)
				else:
					print("sheet列头和用例关键字不一致，不纳入用例sheet。\nsheet列头：%s\n用例关键字：%s" % (sheet_head, self.case_keywords))
			except Exception:
				print("《%s》内容为空，不纳入用例sheet" % name)
		return case_sheets_name
	
	def get_case_content_by_case_sheet(self, case_sheet_name):
		sheet_case_content = []
		sheet_obj = self.excel_case.sheet_by_name(case_sheet_name)
		sheet_case_count = len(sheet_obj.col_values(0)) - 1
		if sheet_case_count:
			for i in range(sheet_case_count):
				sheet_case_content.append(dict(zip(self.case_keywords, sheet_obj.row_values(i + 1))))
			return sheet_case_content

	def get_all_case_content(self):
		excel_case_content = []
		for case_sheet in self.get_case_sheets_name():
			excel_case_content += self.get_case_content_by_case_sheet(case_sheet)
		return excel_case_content

