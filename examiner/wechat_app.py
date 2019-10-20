#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""
import time

import schedule

from examiner.config import Config
from examiner.notification import notification_factory


def get_data(app_names: list):
    os_notification = notification_factory(app_names)
    info_list = os_notification.get_target_notification()
    for each in info_list:
        print(each)


def run(app_names: list):
    schedule.every(Config.INTERVAL).seconds.do(get_data, app_names)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    app_names = ["WeChat"]
    # run(app_names)
    get_data(app_names)
