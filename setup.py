#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-22.
"""

from setuptools import find_packages, setup

setup(
    name="examiner",
    version="0.0.1",
    description="操作系统通知中心监控（不论微信、钉钉、QQ，只要开启消息通知），可编写对应处理脚本",
    install_requires=["biplist"],
    author="Howie Hu",
    author_email="xiaozizayang@gmail.com",
    url="https://github.com/howie6879/examiner",
    packages=find_packages(),
)
