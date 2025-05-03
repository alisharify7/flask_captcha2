
class LoggerMixin(object):
    def log(self, message: str) -> None:
        if self.debug:
           return None
        self.__logger(message)
