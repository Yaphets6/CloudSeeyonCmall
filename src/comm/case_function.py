import json
from src.comm.case_model import CaseModel
from src.comm.data_transformation import DataTransformation


class CaseFunction:
	
	def __init__(self, application):
		self.function = application

	def set_case_content_by_case_number(self, case_number):
		case_content = CaseModel.get_case_content(case_number)
		url = "%s%s" % (self.function.application_service, case_content["接口地址"])
		case_params = case_content["参数"]
		params = DataTransformation.set_params_to_dict(case_params)
		body = dict({"json": {}, "data": {}})
		case_body = case_content["正文"]
		body_value = DataTransformation.set_params_to_dict(case_body)
		body_type = case_content["正文类型"]
		body[body_type] = body_value
		method = case_content["方法"]
		case_request_content = {"url": url, "user": case_content["用户名"], "password": case_content["密码"],
			                    "method": method, "params": params, "body_type": body_type, "body": body,
			                    "case_content": case_content}
		return case_request_content
	
	def function_all_case(self):
		pass
	
	def function_case_by_number(self, case_number):
		request_content = self.set_case_content_by_case_number(case_number)
		url = request_content["url"]
		method = request_content["method"]
		params = request_content["params"]
		body = request_content["body"]
		print("执行用例：%s\n请求方法：%s\n请求正文内容：%s" % (request_content["case_content"]["用例标题"], method,
		                                       str(body[request_content["body_type"]])))
		self.function.set_application_session(request_content["user"], request_content["password"])
		case_response = self.function.request(method=method, url=url, params=params, data=body["data"], json=body["json"],
		                             timeout=3)
		print(case_response.text)
		return case_response
	
	def case_response_text_contains_except(self, response_text, except_text):
		assert except_text in response_text

