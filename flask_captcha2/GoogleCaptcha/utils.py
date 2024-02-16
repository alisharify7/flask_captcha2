from flask import Flask


class CommonCaptchaUtils:
    """Common Method that Both CaptchaV2 and CaptchaV3 classed uses."""

    def refresh_conf(self, app: Flask) -> None:
        """Refresh the captcha object setting using the flask-application configuration"""
        self.__init__(app)


    def debug_log(self, message: str):
        """print log in debug mode only when CAPTCHA_LOG is set to `True`"""
        if self.CAPTCHA_LOG:
            self.Logger.debug(message)