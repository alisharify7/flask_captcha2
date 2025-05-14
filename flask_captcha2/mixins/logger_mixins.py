import logging
from flask_captcha2.logger import get_logger

class LoggerMixin(object):

    def create_logger_object(self, name: str, log_level: int = logging.DEBUG, **kwargs) -> logging.Logger:
        self.logger = get_logger(
            log_level=log_level,
            logger_name=name,
            **kwargs
        )


    def log(self, message: str) -> None:
        if self.DEBUG:
           return None
        self.logger.debug(message)
