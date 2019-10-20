#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""


import hashlib
import platform


def gen_md5(string):
    hl = hashlib.md5()
    hl.update(string.encode(encoding="utf-8"))
    return hl.hexdigest()


def get_os_type():
    os_info = platform.system()
    if os_info == "Darwin":
        return "mac"
    elif os_info == "Windows":
        return "win"
    elif os_info == "Linux":
        return "linux"
    else:
        return "others"


if __name__ == "__main__":
    get_os_type()
