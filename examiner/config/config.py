#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""
import os


class Config:
    DB_PATH = os.environ.get(
        "DB_PATH",
        "/private/var/folders/df/mlv1x3qs1nl3jsyzgz9rpy0h0000gn/0/com.apple.notificationcenter/db2/db",
    )
    INTERVAL = int(os.environ.get("INTERVAL", 60))
    MAC_DB_CMD = "echo `getconf DARWIN_USER_DIR`com.apple.notificationcenter/db2"
