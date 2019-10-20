#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""

import sqlite3

from examiner.config import Config


class SqliteBase:
    def __init__(self, db_path: str = None):
        """连接数据库"""
        if db_path is None:
            db_path = Config.DB_PATH
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def exec_sql(self, sql):
        return self.cur.execute(sql)
