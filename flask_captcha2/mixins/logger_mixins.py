import logging
from flask_captcha2.logger import get_logger


class LoggerMixin(object):
    """Logger Mixin"""

    def create_logger_object(
        self, logger_name: str, logger_level: int = logging.DEBUG, **kwargs
    ) -> logging.Logger:
        return get_logger(log_level=logger_level, logger_name=logger_name, **kwargs)

    def debug_log(self, message: str) -> None:
        if self.CAPTCHA_LOG:
            self.logger.debug(message)
