from src.comm.data_base_handle import MysqlBase
from src.comm.data_transformation import DataTransformation
import re


class CaseModel:
    DEFAULT_CASE_TABLE_COL_HEAD_DISPLAY_NAME = ('用例ID', '用例编号', '用例标题', '用户名', '密码', '应用类型',
                                                '接口地址', '方法', '参数', '正文类型', '正文',  '期望值', '实际值', '执行结果')
    DEFAULT_CASE_TABLE_COL_HEAD_DB_NAME = ('CASE_ID', 'CASE_NUMBER', 'CASE_TITLE', 'USER_NAME', 'PASS_WORD',
                                           'APPLICATION_TYPE', 'INTERFACE_PATH', 'REQUEST_METHOD', 'PARAMS',
                                           'BODY_TYPE', 'BODY', 'EXCEPT_RESPONSE', 'ACTUAL_RESPONSE', 'TEST_RESULT')
    DEFAULT_CASE_TABLE_NAME = "case_info_base"
    DEFAULT_CASE_FUNCTION_RESULT_TABLE = "case_function_result"
    case_info_1 = "CREATE TABLE %s" % DEFAULT_CASE_TABLE_NAME
    case_info_2 = "(%s INT(11) NOT NULL," \
                  "%s VARCHAR(255) NOT NULL PRIMARY KEY," \
                  "%s VARCHAR(255) NOT NULL," \
                  "%s VARCHAR(20)," \
                  "%s VARCHAR(255)," \
                  "%s VARCHAR(20) NOT NULL," \
                  "%s VARCHAR(255) NOT NULL," \
                  "%s VARCHAR(20) NOT NULL," \
                  "%s VARCHAR(225)," \
                  "%s VARCHAR(20)," \
                  "%s LONGTEXT," \
                  "%s LONGTEXT," \
                  "%s LONGTEXT," \
                  "%s INT(10))" % DEFAULT_CASE_TABLE_COL_HEAD_DB_NAME
    CREATE_CASE_BASE_TABLE_SQL = case_info_1 + case_info_2

    @staticmethod
    #   根据获取用例关键字对应的值
    def get_case_attribute_by_case_number(case_number, attribute_name):
        if attribute_name:
            try:
                case_result = CaseModel.get_case_content(case_number)[attribute_name]
                return case_result
            except Exception:
                raise Exception("用例关键字不正确,当前用例有以下关键字:\n %s" % str(CaseModel.DEFAULT_CASE_TABLE_COL_HEAD_DISPLAY_NAME))
        else:
            raise Exception("用例关键字不能为空")

    @staticmethod
    #   获取一条用例内容
    def get_case_content(case_number):
        case_db = MysqlBase()
        case_content = {}
        dict1 = {}
        sql = "SELECT %s FROM %s WHERE CASE_NUMBER = '%s';" % ('*', CaseModel.DEFAULT_CASE_TABLE_NAME, case_number)
        result = case_db.get_mysql_execute_result(sql)
        if len(result) != 1:
            raise Exception("根据用例编号【%s】查询出来的用例数据为空或不唯一：'{}'".format(result))
        else:
            case_result = result[0]
            for i, y in zip(case_result, CaseModel.DEFAULT_CASE_TABLE_COL_HEAD_DISPLAY_NAME):
                dict1[y] = i
                case_content.update(dict1)
            case_db.close_mysql_db(case_db)
            return case_content

    @staticmethod
    #   获取所有用例编号
    def get_all_case_number():
        sql = "SELECT CASE_NUMBER FROM %s;" % CaseModel.DEFAULT_CASE_TABLE_NAME
        mysql_db = MysqlBase()
        search_result = mysql_db.get_mysql_execute_result(sql)
        if search_result:
            case_number_list = DataTransformation.get_tuple_value(search_result)
            return case_number_list
        else:
            return []

    @staticmethod
    # 更新数据库中的用例数据，先删再插入
    def update_case_by_content(case_content):
        case_number = case_content['用例编号']
        mysql_db = MysqlBase()
        CaseModel.delete_case_by_case_number(case_number)
        sql = CaseModel.get_insert_case_content_sql(case_content)
        mysql_db.execute_sql(sql)
        mysql_db.close_mysql_db(mysql_db)

    @staticmethod
    #   根据用例编号删除用例表中对应的数据
    def delete_case_by_case_number(case_number):
        if case_number:
            try:
                mysql_db = MysqlBase()
                sql_2 = "DELETE FROM %s WHERE CASE_NUMBER = '%s';" % (CaseModel.DEFAULT_CASE_TABLE_NAME, case_number)
                mysql_db.execute_sql(sql_2)
            except Exception:
                raise Exception("未能找到编号为:‘%s’的用例数据" % case_number)
        else:
            raise Exception("用例编号不能为空")

    @staticmethod
    def get_insert_case_content_sql(case_content):
        value_list = []
        for value in case_content.values():
            value_list.append(value)
        value_list = tuple(value_list)
        str_1 = "INSERT INTO %s" % CaseModel.DEFAULT_CASE_TABLE_NAME
        str_2 = re.sub(r"\'", "", "%s" % str(CaseModel.DEFAULT_CASE_TABLE_COL_HEAD_DB_NAME))
        str_3 = " VALUES "
        str_4 = "%s;" % str(value_list)
        sql = str_1 + str_2 + str_3 + str_4
        return sql
    
    @staticmethod
    def get_application_case(application_name):
        mysql_db = MysqlBase()
        sql = "SELECT case_number FROM %s WHERE APPLICATION_TYPE = '%s'" % (CaseModel.DEFAULT_CASE_TABLE_NAME, application_name)
        return DataTransformation.get_tuple_value(mysql_db.get_mysql_execute_result(sql))
        
    @staticmethod
    def initialization_case_base_table():
        mysql_db = MysqlBase()
        try:
            mysql_db.execute_sql("TRUNCATE TABLE %s;" % CaseModel.DEFAULT_CASE_TABLE_NAME)
        except:
            mysql_db.execute_sql(CaseModel.CREATE_CASE_BASE_TABLE_SQL)
        mysql_db.close_mysql_db(mysql_db)

