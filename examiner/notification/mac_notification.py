#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""
import os
import plistlib

from datetime import datetime

from biplist import readPlistFromString

from examiner.config import Config
from examiner.databases import SqliteBase
from examiner.notification.base_notification import BaseNotification
from examiner.utils import exec_cmd, gen_md5, logger


class MacNotification(BaseNotification):
    def __init__(self, app_names: list, db_cmd: str = None):
        self.db_cmd = db_cmd or Config.MAC_DB_CMD
        self.db_path = self._get_db_path()
        self.sqlite_base = SqliteBase(self.db_path)
        self.app_identifier_dict, self.app_id_dict = self._process_app_names(app_names)

    def _get_db_path(self):
        # cmd = "lsof -p $(ps aux | grep -m1 usernoted | awk '{ print $2 }')| awk '{ print $9 }' | grep 'db2/db$' | xargs dirname"
        _, stdout = exec_cmd(self.db_cmd)
        db_path = os.path.join(stdout, "db")
        return db_path

    def _process_app_names(self, app_names: list):
        app_identifier_dict, app_id_dict = {}, {}
        for app_name in app_names:
            info_plist = f"/Applications/{app_name}.app/Contents/Info.plist"
            if os.path.exists(info_plist):
                with open(info_plist, "rb") as fp:
                    pl = plistlib.load(fp)
                    app_identifier = pl["CFBundleIdentifier"]
                    app_identifier_dict[app_identifier.lower()] = {"app_name": app_name}
            else:
                logger.error(f"文件 {info_plist} 不存在，请判断 {app_name} 是否安装")
        if app_identifier_dict:
            """获取所有app的字典信息"""
            sql_str = """SELECT DISTINCT (SELECT identifier FROM app WHERE app.app_id = record.app_id) AS app, app_id FROM record"""
            cursor = self.sqlite_base.cur.execute(sql_str)

            for row in cursor:
                if row["app"] in app_identifier_dict.keys():
                    app_identifier_dict[row["app"]]["app_id"] = row["app_id"]
                    app_id_dict[row["app_id"]] = row["app"]
        return app_identifier_dict, app_id_dict

    def _process_db_param(self, param):
        # TODO
        # return param.replace("\t", " ").replace("\r", " ").replace("\n", "")
        return param

    def _process_db_time(self, time):
        date = datetime.fromtimestamp(time + 978307200)
        return date

    def get_notifications(self):
        """获取监控的目标app的所有监控中心的消息"""
        app_ids = ",".join(str(i) for i in self.app_id_dict.keys())
        sql_str = f"""
        SELECT app_id,data, presented, delivered_date FROM record WHERE app_id IN ({app_ids})  ORDER BY delivered_date DESC;
        """
        cursor = self.sqlite_base.cur.execute(sql_str)
        info_list = []
        for row in cursor:
            info_dict = self.process_db_row(row)
            info_list.append(info_dict)
        return info_list

    def process_db_row(self, row_data):
        plist = readPlistFromString(row_data["data"])
        try:
            req = plist["req"]
            title = self._process_db_param(req.get("titl", ""))
            subtitle = self._process_db_param(req.get("subt", ""))
            body = self._process_db_param(req.get("body", ""))
            delivered_date = self._process_db_time(row_data["delivered_date"] or 0)
            app_identifier = self.app_id_dict[row_data["app_id"]]
            info_dict = dict(
                title=title,
                subtitle=subtitle,
                body=body,
                delivered_date=delivered_date,
                presented=row_data["presented"],
                app_identifier=app_identifier,
                app_name=self.app_identifier_dict[app_identifier]["app_name"],
                md5=gen_md5(f"{title}-{subtitle}-{body}-{delivered_date}"),
            )
            return info_dict
        except Exception as e:
            logger.exception(f"消息解析出错：{e}")
            return None


if __name__ == "__main__":
    mac_notification = MacNotification(app_names=["WeChat", "DingTalk"])
    info_list = mac_notification.get_notifications()
    print(info_list)
