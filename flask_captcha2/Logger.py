import logging
import sys


def get_logger(LogLevel, CaptchaName: str = "Flask-Captcha") -> logging.Logger:
    """ This function return a stdout Logger
    args:
        . CaptchaName:string: name of the logger
    """
    logLevel = LogLevel or logging.DEBUG
    logformat = logging.Formatter(f"[{CaptchaName}" + "- %(levelname)s] [%(asctime)s] - %(message)s")
    logger = logging.getLogger(CaptchaName)
    logger.setLevel(logLevel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logLevel)
    handler.setFormatter(logformat)
    logger.addHandler(handler)
    return logger
