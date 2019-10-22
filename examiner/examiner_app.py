#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-22.
"""

from examiner.config import Config
from examiner.notification import notification_factory
from examiner.utils import logger


class Examiner:
    """
    入口
    """

    def __init__(self, app_names: list):
        self.config = Config
        self.logger = logger
        self.app_names = app_names
        self.os_notification = notification_factory(app_names)

    def get_notifications(self):
        return self.os_notification.get_notifications()
