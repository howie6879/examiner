#!/usr/bin/env python
"""
 Created by howie.hu at 2019-10-20.
"""

import logging


def get_logger(name="examiner"):
    logging_format = "[%(asctime)s] %(levelname)-5s %(name)-5s"
    # logging_format += "%(module)-7s::l%(lineno)d: "
    # logging_format += "%(module)-7s: "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format, level=logging.INFO, datefmt="%Y:%m:%d %H:%M:%S"
    )
    logging.getLogger("schedule").setLevel(logging.ERROR)
    return logging.getLogger(name)


logger = get_logger()
