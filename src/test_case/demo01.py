import requests
import unittest
import xlrd
import json
import html
import xmltodict

class demo(unittest.TestCase):

    def test_case001(self):

        """加载用例"""
        xl = xlrd.open_workbook("F:\接口\接口Demo1.xlsx")
        datas = xl.sheets()[1]
        rows = datas.nrows
        """ 获取用例数量"""
        case_no = datas.ncols
        titles = datas.row_values(0)
        print("列数" + str(case_no))
        print(titles)
        for col in range(case_no):
            if(titles[col] == "用例编号"):
                case_no_col = col
                print(col)
                break
        """获取所有用例编号"""
        case_name = datas.col_values(case_no_col)
        del case_name[0]
        print(case_name)

        """根据用例编号获取用例数据"""
        case_row_no = case_name.index("uc_center_001")
        print(case_row_no)
        case_value = datas.row_values(case_row_no)
        case_dict = {}
        for title in titles:
            case_dict[title] = case_value[titles.index(title)]
        print(case_dict)
        """根据用例编号执行用例"""
        print("执行用例:" + case_dict['用例编号'] + "\r")
        print("测试内容:" + case_dict['用例标题'] + "\r")
        url = "http://192.168.225.11:8085" + case_dict["接口地址"]
        print("接口地址:" + url + "\r")
        """请求方法封装"""
        print(case_dict['json参数'])
        if(case_dict['方法'] == 'POST'):
            r = requests.post(url,data=case_dict['data参数'],json=json.loads(case_dict['json参数']))
        else:
            r = requests.get(url,data=case_dict['data参数'],json=json.loads(case_dict['json参数']))

        respones_text = r.text
        xml_data = html.unescape(respones_text)
        print("接口返回内容:" + xml_data + "\r")
        """处理xml格式返回数据为json格式"""
        xml = xmltodict.parse(xml_data)
        print(type(xml))

        respones_json = json.dumps(xml, ensure_ascii=False)
        print(xml)
        print("将字OrderedDict换为json格式:" + respones_json + "\r")
        respone_dict = json.loads(respones_json, encoding="utf-8")
        datas = DataCenter()

        print(datas.get_target_value('orgid',respone_dict,[]))
        assert_data = json.loads(case_dict["检查点"], encoding='utf-8')
        print(type(assert_data))
        i = 1
        for key in assert_data.keys():
            print("第%s个检查key:%s" % (i, key))
            assert assert_data[key] == datas.get_value_by_key(respone_dict,key)
            i += 1

