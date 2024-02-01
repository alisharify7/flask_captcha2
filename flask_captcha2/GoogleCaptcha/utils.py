from flask import Flask


class CommandCaptchaUtils:
    """Common Method that Both CaptchaV2 and CaptchaV3 uses"""
    def refresh_conf(self, app:Flask):
        self.__init__(app)