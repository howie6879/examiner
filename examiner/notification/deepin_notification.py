#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-27.
"""

from datetime import datetime

from examiner.config import Config
from examiner.databases import SqliteBase
from examiner.utils import exec_cmd, gen_md5
from examiner.notification.base_notification import BaseNotification


class DeepInNotification(BaseNotification):
    def __init__(self, app_names: list, db_cmd: str = None):
        self.db_cmd = db_cmd or Config.DEEPIN_DB_CMD
        self.db_path = self._get_db_path()
        self.sqlite_base = SqliteBase(self.db_path)
        self.app_names = app_names

    def _get_db_path(self):
        _, stdout = exec_cmd(self.db_cmd)
        return stdout

    def _process_db_time(self, time):
        date = datetime.fromtimestamp(int(time[:10]))
        return date

    def get_notifications(self):
        """获取监控的目标app的所有监控中心的消息"""
        app_str = ",".join(f"'{i}'" for i in self.app_names)
        sql_str = f"""
        SELECT * FROM notifications2 WHERE AppName IN ({app_str})  ORDER BY CTime DESC;
        """
        cursor = self.sqlite_base.cur.execute(sql_str)
        info_list = []
        for row in cursor:
            info_dict = self.process_db_row(row)
            info_list.append(info_dict)
        return info_list

    def process_db_row(self, row_data):
        date = self._process_db_time(row_data["CTime"])
        info_dict = {
            "summary": row_data["Summary"],
            "body": row_data["Body"],
            "app_name": row_data["AppName"],
            "date": date,
            "md5": gen_md5(
                f"""{row_data["Summary"]}-{row_data["Body"]}-{row_data["AppName"]}-{date}"""
            ),
        }
        return info_dict


if __name__ == "__main__":
    deepin_notification = DeepInNotification(app_names=["mitalk"])
    info_list = deepin_notification.get_notifications()
    print(info_list)
