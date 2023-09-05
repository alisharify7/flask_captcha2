# -*- coding: utf-8 -*-

import sys
import logging


def get_logger():
    """ Logger """
    logLevel = logging.INFO
    logformat = logging.Formatter("[Flask-Captcha - %(levelname)s] [%(asctime)s] - %(message)s")
    logger = logging.getLogger(__name__)
    logger.setLevel(logLevel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logLevel)
    handler.setFormatter(logformat)
    logger.addHandler(handler)  
    return logger