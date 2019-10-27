#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""

import hashlib
import platform
import subprocess


def exec_cmd(cmd):
    """执行命令"""
    status, stdout = subprocess.getstatusoutput(cmd)
    return status, stdout


def gen_md5(string):
    """对字符串进行md5加密"""
    hl = hashlib.md5()
    hl.update(string.encode(encoding="utf-8"))
    return hl.hexdigest()


def get_os_type():
    """获取系统类型"""
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
