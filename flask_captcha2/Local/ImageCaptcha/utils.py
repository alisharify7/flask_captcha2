import os
import random
import base64
from string import digits, punctuation, ascii_letters

from captcha import image

from flask import Flask, session

from .excp import NotFlaskObject


class ImageCaptchaCONF:
    RECAPTCHA_KEY: str = ""
    RECAPTCHA_ENABLE: str = ""
    RECAPTCHA_LOG: bool = ""
    RECAPTCHA_MIN: int = ""
    RECAPTCHA_MAX: int = ""
    RECAPTCHA_ALPHABET: bool = ""
    RECAPTCHA_PUNCTUATION: bool = ""


class ImageCaptcha(ImageCaptchaCONF):
    def __init__(self, app: Flask = None, RECAPTCHA_KEY="",
                 RECAPTCHA_ENABLE: bool = True, RECAPTCHA_LOG: bool = True, RECAPTCHA_MIN: int = 99999 + 1,
                 RECAPTCHA_MAX: int = 999999 + 1,
                 RECAPTCHA_ALPHABET: bool = False, RECAPTCHA_PUNCTUATION: bool = False
                 ):
        if app:
            self.init_app(app=app)
        else:
            self.RECAPTCHA_PUNCTUATION = RECAPTCHA_ALPHABET
            self.RECAPTCHA_LOG = RECAPTCHA_LOG

        self.IMAGER = ImageCaptcha()

        pass

    def init_app(self, app: Flask):
        if not isinstance(app, Flask):
            raise NotFlaskObject(f"object <{app}> is not a Flask Instance!")

    def __generate(self):
        captchaCode = str(random.randint(self.RECAPTCHA_MIN, self.RECAPTCHA_MAX))
        imageCaptcha = self.IMAGER.generate(captchaCode)
        return base64.b64encode(imageCaptcha.getvalue()).decode('ascii')

    def generate(self):
        return self.__generate()

    def __validate(self):
        pass

    def validate(self):
        ...
