#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""

from examiner.utils import get_os_type
from examiner.notification.base_notification import BaseNotification
from examiner.notification.mac_notification import MacNotification


def notification_factory(app_names: list, **kwargs) -> BaseNotification:
    """返回对应系统的通知类"""
    os_type = get_os_type()
    if os_type == "mac":
        os_notification = MacNotification(app_names=app_names, **kwargs)
    else:
        os_notification = MacNotification(app_names=app_names, **kwargs)
    return os_notification


if __name__ == "__main__":
    notification_factory([])
