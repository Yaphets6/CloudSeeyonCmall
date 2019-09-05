import mysql.connector
from src.confing.mysql_data_base_config import *


class MysqlBase:

    def __init__(self):
        self.host = mysql_host
        self.port = mysql_port
        self.user = mysql_user
        self.password = mysql_password
        self.database = case_base_database_name
        self.mysql_db = self.get_mysql_db()
        self.cursor = self.mysql_db.cursor()

    def get_mysql_db(self):
        return mysql.connector.connect(host=self.host, port=self.port,
                                       user=self.user, password=self.password, database=self.database)

    def get_cursor(self):
        return self.get_mysql_db().cursor()

    def get_mysql_connect_obj(self):
        try:
            self.mysql_db.ping()
            return self
        except Exception:
            print("数据库连接已经关闭，将重新连接")
            new_db = MysqlBase()
            return new_db

    def execute_sql_list(self, sql_list):
        db_boj = self.get_mysql_connect_obj()
        db_boj.cursor.execute(sql_list, multi=True)

    def execute_sql(self, sql):
        db = self.get_mysql_connect_obj()
        db.cursor.execute(sql, multi=False)
        db.mysql_commit()
        db.close_mysql_db(db)

    def mysql_commit(self):
        try:
            self.mysql_db.commit()
        except:
            print("数据库事务提交失败，事务回滚")
            self.mysql_db.rollback()

    def get_mysql_execute_result(self, sql):
        db = self.get_mysql_connect_obj()
        db.cursor.execute(sql, multi=False)
        result = db.cursor.fetchall()
        db.mysql_commit()
        db.close_mysql_db(db)
        return result
        # except Exception:
        #     print("执行sql无查询结果")
        #     db.close_mysql_db(db)
        #     return None

    @staticmethod
    def close_mysql_db(db):
        db.cursor.close()
        db.mysql_db.close()
