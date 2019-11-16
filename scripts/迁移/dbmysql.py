#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import pymssql
from warnings import filterwarnings

filterwarnings('ignore', category=pymysql.Warning)


class mysql_db(object):
    """
    mysql数据库连接,封装类
    """

    def __init__(self, host, port, user, password, db='mysql'):
        self.conn = pymysql.connect(host=host, port=port, database=db, user=user, password=password, charset='utf8',
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()
        self.cur.close()

    def close(self):
        self.conn.commit()
        self.conn.close()
        self.cur.close()

    # select Query one
    def fetch_one(self, sql, params=None):
        self.cur.execute(sql, params)
        return self.cur.fetchone()

    # More than a query
    def fetch_all(self, sql, params=None):
        self.cur.execute(sql, params)
        return self.cur.fetchall()

    # update 1
    def execute_one(self, sql, params=None):
        return self.cur.execute(sql, params)

    # Modify multiple
    def execute_many(self, sql, params=None):
        return self.cur.executemany(sql, params)


class sql_server_db(object):
    """
    sql server数据库连接,封装类
    """

    def __init__(self, host, port, user, password, db='ReportServer'):
        self.conn = pymssql.connect(host=host, port=port, user=user, password=password, database=db, charset='utf8')
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()
        self.cur.close()

    def close(self):
        self.conn.commit()
        self.conn.close()
        self.cur.close()

    def fetch_one(self, sql, params=None):
        self.cur.execute(sql, params)
        return self.cur.fetchone()

    def fetch_all(self, sql, params=None):
        self.cur.execute(sql, params)
        return self.cur.fetchall()

    def execute_one(self, sql, params=None):
        return self.cur.execute(sql, params)

    def execute_many(self, sql, params=None):
        return self.cur.executemany(sql, params)
