from src.confing.application_service_config import *
from requests.sessions import Session
import re


class Application(Session):

	def __init__(self, application_name):
		self.application_info = applications_data[application_name]
		service = list(self.application_info["service"].values())
		self.application_service = "%s://%s:%s" % tuple(service)
		Session.__init__(self)
	
	def set_application_login_body(self):
		login_body = dict({"data": {}, "json": {}})
		body_values = self.application_info["login"]["body"]["values"]
		body_type = self.application_info["login"]["body"]["type"]
		login_body[body_type] = body_values
		return login_body
	
	def set_application_session(self, user, password):
		pass
	
	def verify_status(self):
		if self.application_info["service"]["connect_type"] == "https":
			return False
		else:
			return True
		

class DeeApplication(Application):
	def __init__(self):
		Application.__init__(self, "DEE")


class V5Application(Application):
	def __init__(self):
		Application.__init__(self, "V5")
		
	def set_v5_application_login_body(self, user, password):
		self.application_info["login"]["body"]["values"]["login_username"] = user
		self.application_info["login"]["body"]["values"]["login_password"] = password
		return self.set_application_login_body()
	
	def set_application_session(self, user, password):
		login_path = self.application_info["login"]["path"]
		if login_path == "":
			print("《%s》应用服务接口调，用无需身份验证" % self.application_info["application_name"])
		else:
			login_url = "%s%s" % (self.application_service, self.application_info["login"]["path"])
			params = self.application_info["login"]["params"]
			login_body = self.set_v5_application_login_body(user, password)
			self.post(url=login_url, params=params, data=login_body["data"], json=login_body["json"],
			          headers=self.application_info["headers"], timeout=6, verify=self.verify_status)
	

class CHomeApplication(Application):
	
	def __init__(self):
		Application.__init__(self, "CHOME")
	
	def get_login_page_form_token(self):
		login_page_url = "%s%s" % (self.application_service, "/portal.php?m=user&a=login")
		verify = self.verify_status()
		response = self.get(url=login_page_url, timeout=6, verify=verify)
		form_token = re.findall("[0-9a-zA-z]{32,}", response.text)
		return form_token[0]

	def set_c_home_application_login_body(self, user, password):
		self.application_info["login"]["body"]["values"]["username"] = user
		self.application_info["login"]["body"]["values"]["password"] = password
		self.application_info["login"]["body"]["values"]["form_token"] = self.get_login_page_form_token()
		return self.set_application_login_body()
	
	def set_application_session(self, user, password):
		login_path = self.application_info["login"]["path"]
		if login_path == "":
			print("《%s》应用服务接口调，用无需身份验证" % self.application_info["application_name"])
		else:
			login_url = "%s%s" % (self.application_service, self.application_info["login"]["path"])
			params = self.application_info["login"]["params"]
			login_body = self.set_c_home_application_login_body(user, password)
			c_home_response = self.post(url=login_url, params=params, data=login_body["data"], json=login_body["json"],
			                            timeout=6, verify=False)
			c_home_token = "Bearer " + c_home_response.json()["token"]["refresh_token"]
			self.application_info["headers"]["Authorization"] = c_home_token
			new_headers = self.application_info["headers"]
			self.headers = new_headers
