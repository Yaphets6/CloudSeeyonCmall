

#   DEE服务器接口配置信息
dee_service = {"connect_type": "http", "host": "192.168.225.11", "port": "8085"}
dee_request_headers = {"Content-Type": "application/json"}
dee_request_cookies = {"Cookies": ""}
dee_login = {"path": "", "parameter_type": "", "login_token": ""}
DEE = {"service": dee_service, "headers": dee_request_headers,
       "cookies": dee_request_cookies, "login": dee_login, "application_name": "DEE"}

#   v5服务器接口配置信息
v5_service = {"connect_type": "http", "host": "seeyonapp.seeyon.com", "port": "80"}
v5_request_headers = {"Connection": "keep-alive",
                      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                      "Accept-Encoding": "gzip, deflate",
                      "Accept-Language": "zh-CN,zh;q=0.9",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
v5_request_cookies = {"JSESSIONID": ""}
v5_login = {"path": "/seeyon/main.do", "params": {"method": "login"},
            "body": {"type": "data", "values": {"login_username": "", "login_password": ""}}}
V5 = {"service": v5_service, "headers": v5_request_headers,
      "cookies": v5_request_cookies, "login": v5_login, "application_name": "V5"}


#   用户中心服务器接口配置
chome_service = {"connect_type": "https", "host": "chome.seeyon.com", "port": "443"}
chome_request_headers = {"Connection": "keep-alive",
                         "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                         "Accept-Encoding": "gzip, deflate",
                         "Accept-Language": "zh-CN,zh;q=0.9",
                         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
                         "Authorization": ""}
chome_login = {"path": "/portal.php", "params": {"m": "user","a":"loginSub"},
               "body": {"type": "data", "values": {"account_type": "1", "username": "", "password": "", "form_token": ""}}}

chome_cookies = {""}
CHOME = {"service": chome_service, "headers": chome_request_headers,
         "cookies": v5_request_cookies, "login": chome_login, "application_name": "CHOME"}
applications_data = {"DEE": DEE, "V5": V5, "CHOME": CHOME}
