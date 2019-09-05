import xmltodict
import html
import json


class DataTransformation:

    @staticmethod
    def get_value_by_key(key, dic):
        """
        key: 目标key值
        dic: 遍历的字典数据
        :return: str
        """
        if key in dic.keys():
            return dic[key]
        else:
            for value in dic.values():
                if isinstance(value, dict):
                    #   每次递归需要调用return方法，避免返回值为None
                    return DataTransformation.get_value_by_key(key, value)

    @staticmethod
    def get_target_value(key, dic, tmp_list):
        """
        :param key: 目标key值
        :param dic: JSON数据j
        :param tmp_list: 用于存储获取的数据
        :return: list
        """
        if not isinstance(dic, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
            return 'argv[1] not an dict or argv[-1] not an list '

        if key in dic.keys():
            tmp_list.append(dic[key])  # 传入数据存在则存入tmp_list
        else:
            for value in dic.values():  # 传入数据不符合则对其value值进行遍历
                if isinstance(value, dict):
                    DataTransformation.get_target_value(key, value, tmp_list)  # 传入数据的value值是字典，则直接调用自身
                elif isinstance(value, (list, tuple)):
                    DataTransformation._get_value(key, value, tmp_list)  # 传入数据的value值是列表或者元组，则调用_get_value
        return tmp_list

    @staticmethod
    def _get_value(key, val, tmp_list):
        for val_ in val:
            if isinstance(val_, dict):
                DataTransformation.get_target_value(key, val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
            elif isinstance(val_, (list, tuple)):
                DataTransformation._get_value(key, val_, tmp_list)  # 传入数据的value值是列表或者元组，则调用自身

    @staticmethod
    def change_response_xml_to_json(response_xml):
        response_dict = DataTransformation.format_xml_to_dict(DataTransformation.format_xml_str(response_xml))
        response_json = DataTransformation.format_json_str_to_json(response_dict)
        return response_json

    @staticmethod
    def format_xml_str(xml_str):
        # 先将中文转码，转为标准xml格式
        return html.unescape(xml_str)

    @staticmethod
    def format_xml_to_dict(xml_str):
        # 将标准html格式转为字典格式
        return xmltodict.parse(xml_str, encoding="utf-8")

    @staticmethod
    def format_dict_to_json_str(response_dict):
        # 将字典格式内容转为json字符串
        return json.dumps(response_dict, ensure_ascii=False)

    @staticmethod
    def format_json_str_to_json(json_str):
        # 将json字符串转换为json类型
        return json.loads(json_str, encoding="utf-8")

    @staticmethod
    def change_tuple(tuple_data):
        if isinstance(tuple_data, (tuple, list)):
            for value in tuple_data:
                return DataTransformation.change_tuple(value)
        else:
            return tuple_data

    @staticmethod
    # 获取元组对象的值，组成一个list
    def get_tuple_value(data_tuple):
        if isinstance(data_tuple, (tuple, list)):
            list_data = []
            for value in data_tuple:
                list_data.append(DataTransformation.change_tuple(value))
            return list_data
        else:
            raise Exception("'%s'不是列表或者元组类型")
    
    @staticmethod
    def set_params_to_dict(str_data):
        if str_data:
            if isinstance(str_data, dict):
                return str_data
        else:
            return dict({})
