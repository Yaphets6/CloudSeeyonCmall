import xlwt
from src.comm.project_path import ProjectPath
from src.comm.data_base_handle import MysqlBase
import re
from src.comm.data_transformation import DataTransformation


class CaseModel:
	#   用例内容表名
	case_info_table_name = "case_info"
	#   用例执行结果表名
	case_result_table_name = "case_result"
	#   定义用例内容表结构
	keywords_dict = {
		"用例编号": {"header_name": "case_number", "type": "VARCHAR(255)", "enable_null": "not null"},
		"用例标题": {"header_name": "case_title", "type": "VARCHAR(255)", "enable_null": "not null"},
		"用户名": {"header_name": "user_name", "type": "VARCHAR(255)", "enable_null": ""},
		"密码": {"header_name": "password", "type": "VARCHAR(50)", "enable_null": ""},
		"应用类型": {"header_name": "application_type", "type": "VARCHAR(50)", "enable_null": "not null"},
		"接口地址": {"header_name": "interface_path", "type": "VARCHAR(255)", "enable_null": "not null"},
		"方法": {"header_name": "request_method", "type": "VARCHAR(20)", "enable_null": "not null"},
		"参数": {"header_name": "request_params", "type": "VARCHAR(255)", "enable_null": ""},
		"正文类型": {"header_name": "request_body_type", "type": "VARCHAR(20)", "enable_null": ""},
		"正文": {"header_name": "request_body", "type": "longtext", "enable_null": ""},
		"期望值类型": {"header_name": "except_response_type", "type": "VARCHAR(20)", "enable_null": "not null"},
		"期望值": {"header_name": "except_response", "type": "longtext", "enable_null": "not null"},
		"实际值": {"header_name": "actual_response", "type": "longtext", "enable_null": "not null"}
	}
	#   定义用例结果表结构
	result_dict = {
		"用例编号": {"header_name": "case_number", "type": "VARCHAR(255)", "enable_null": "not null"},
		"用例标题": {"header_name": "case_title", "type": "VARCHAR(255)", "enable_null": "not null"},
		"应用类型": {"header_name": "application_type", "type": "VARCHAR(50)", "enable_null": "not null"},
		"用例执行结果": {"header_name": "request_body", "type": "longtext", "enable_null": ""}
	}

	header_list = []
	for i in list(keywords_dict.values()):
		header_list.append(i["header_name"])
	
	def __init__(self):
		self.info_table_name = CaseModel.case_info_table_name
		self.result_table_name = CaseModel.case_result_table_name
		self.keywords_dict = CaseModel.keywords_dict
		self.case_keywords = list(CaseModel.keywords_dict.keys())
		self.result_dict = CaseModel.result_dict
		self.result_keywords = CaseModel.result_dict.keys()
		self.header_list = CaseModel.header_list
	
	#   生成excel用例模板文件
	def generate_excel_case_file_model(self):
		#   用例存储路径
		case_file_name = "用例模板.xlsx"
		path = ProjectPath.case_files_path() + case_file_name
		#   初始化excel用例模板文件
		excel_case_model = xlwt.Workbook()
		case_sheet = excel_case_model.add_sheet("用例模板_用例内容");
		keywords = self.case_keywords
		y = 0
		for keyword in keywords:
			case_sheet.write(0, y, keyword)
			y += 1
		print("Excel用例模板文件将生成到——————————————》%s" % path)
		excel_case_model.save(path)
	
	#   创建用例内容基础表
	def create_case_info_table(self):
		mysql = MysqlBase()
		drop_table = "DROP TABLE IF EXISTS %s;" % self.info_table_name
		sql = "CREATE TABLE %s(CASE_ID INT(11) not null PRIMARY KEY AUTO_INCREMENT);" % self.info_table_name
		mysql.execute_sql(drop_table)
		mysql.execute_sql(sql)
		
	#   创建用例执行结果基础表
	def create_case_result_table(self):
		mysql = MysqlBase()
		drop_table = "DROP TABLE IF EXISTS %s;" % self.result_table_name
		sql = "CREATE TABLE %s(CASE_ID INT(11) not null PRIMARY KEY AUTO_INCREMENT);" % self.result_table_name
		mysql.execute_sql(drop_table)
		mysql.execute_sql(sql)
	
	# 基于用例内容基础表，新增用例字段
	def add_case_info_table(self, key):
		table_field_info = self.keywords_dict[key]
		sql_1 = "ALTER TABLE %s " % self.info_table_name
		sql_2 = "ADD %s %s %s;" % tuple(table_field_info.values())
		mysql = MysqlBase()
		mysql.execute_sql(sql_1 + sql_2)
		
	#   基于用例执行结果基础表，新增执行结果字段（通过主键【CASE_ID】,关联查询用例信息）
	def add_case_result_table(self, key):
		table_field_info = self.result_dict[key]
		sql_1 = "ALTER TABLE %s " % self.result_table_name
		sql_2 = "add %s %s %s;" % tuple(table_field_info.values())
		mysql = MysqlBase()
		mysql.execute_sql(sql_1 + sql_2)
		
	#   初始化用例内容表,删除原有表，新建。
	def initialization_case_info_table(self):
		try:
			self.create_case_info_table()
			for key in self.case_keywords:
				self.add_case_info_table(key)
		except Exception:
			raise Exception("初始化用例内容表失败，数据暂时手动回滚")
			
	#   初始化用例执行结果表，删除原有表，新建。
	def initialization_case_result_table(self):
		try:
			self.create_case_result_table()
			for key in self.result_keywords:
				self.add_case_result_table(key)
		except Exception:
			raise Exception("初始化用例执行结果表失败，数据暂时手动回滚")

	#	拼接插入用例内容sql
	def insert_case_info_sql(self, insert_values):
		sql_1 = "INSERT INTO %s" % CaseModel.case_info_table_name
		sql_2 = re.sub(r"\'", "", str(tuple(self.get_case_info_table_headers())))
		print(insert_values)
		sql_3 = " VALUES %s;" % str(tuple(insert_values))
		insert_sql = sql_1 + sql_2 + sql_3
		print(insert_sql)
		return insert_sql

	#	获取用例内容表的表头，用于拼接SQL。
	def get_case_info_table_headers(self):
		header_list = []
		for i in list(self.keywords_dict.values()):
			header_list.append(i["header_name"])
		return header_list

	def get_case_content_from_case_info(self):
		mysql = MysqlBase()
		case_info_header = self.get_case_info_table_headers()
		case_info_header.insert(0, "CASE_ID")
		all_content = mysql.get_mysql_execute_result("SELECT * FROM %s WHERE CASE_ID != '' OR CASE_ID != NULL" %
																self.case_info_table_name)
		case_content = []
		for content in all_content:
			case_content.append(dict(zip(case_info_header, content)))
		return case_content

	def get_case_total_from_case_info(self):
		case_total = len(self.get_case_content_from_case_info())
		return case_total

	def get_cases_number_list(self):
		mysql = MysqlBase()
		sql_result = mysql.get_mysql_execute_result("SELECT case_number FROM %s WHERE CASE_ID != '' OR CASE_ID != NULL;" % self.case_info_table_name)
		cases_number = DataTransformation.get_tuple_value(sql_result)
		return cases_number

	def get_case_content_by_case_number(self, case_number):
		mysql = MysqlBase()
		sql_result = mysql.get_mysql_execute_result("SELECT * FROM %s WHERE case_number = '%s';" % (self.case_info_table_name, case_number))
		case_headers = self.header_list
		case_headers.insert(0, "CASE_ID")
		case_content = dict(zip(case_headers, DataTransformation.get_tuple_value(sql_result)))
		print(case_content)
		return case_content
