#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""

import abc


class BaseNotification:
    @abc.abstractmethod
    def get_notifications(self, **kwargs):
        pass
