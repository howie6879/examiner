#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""
import time

import schedule

from examiner import Examiner


def get_data(app_names: list):
    examiner_app = Examiner(app_names)
    info_list = examiner_app.get_notifications()
    for each in info_list:
        print(each)


def run(app_names: list):
    schedule.every(10).seconds.do(get_data, app_names)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run(["Wechat"])
