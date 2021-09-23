#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""

from examiner.notification.base_notification import BaseNotification
from examiner.notification.deepin_notification import DeepInNotification
from examiner.notification.mac_notification import MacNotification
from examiner.utils import exec_cmd, get_os_type


def notification_factory(app_names: list, **kwargs) -> BaseNotification:
    """返回对应系统的通知类"""
    os_type = get_os_type()
    os_notification = None
    if os_type == "mac":
        os_notification = MacNotification(app_names=app_names, **kwargs)
    elif os_type == "linux":
        sys_info = exec_cmd("uname -a")
        if "deepin" in sys_info:
            os_notification = DeepInNotification(app_names=app_names, **kwargs)
        else:
            exit("examiner 暂时还不支持此系统，具体可点击：https://github.com/howie6879/examiner 进行反馈")
    else:
        exit("examiner 暂时还不支持此系统，具体可点击：https://github.com/howie6879/examiner 进行反馈")
    return os_notification


if __name__ == "__main__":
    notification_factory([])
