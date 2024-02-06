import os
import random
import base64
import string

# libs
from captcha import image
from flask import Flask, session
from captcha.image import ImageCaptcha


# flask-captcha2
from . import excp as ex
from flask_captcha2.Logger import get_logger


class BaseImageCaptcha:
    RECAPTCHA_ENABLE: bool = True
    RECAPTCHA_LOG: bool = True
    RECAPTCHA_LENGTH: int = 6

    RECAPTCHA_INCLUDE_LETTERS: bool = True
    RECAPTCHA_INCLUDE_NUMERIC: bool = False
    RECAPTCHA_INCLUDE_PUNCTUATION: bool = False

    _alphabet:str = string.ascii_lowercase
    _punctuation:str = string.punctuation
    _numbers :str= string.digits
    _imgGeneratorEngine: ImageCaptcha = None

    Logger = get_logger("Flask-Captcha2-ImageCaptcha")

    def random_number(self, length: int) -> list:
        """return a list contains only numbers randomly with fixed length of input args """
        return random.choices(self._numbers, k=length)

    def random_punctuation(self, length: int) -> list:
        """return a list contains only punctuation randomly with fixed length of input args """
        return random.choices(self._punctuation, k=length)

    def random_alphabet(self, length: int) -> list:
        """return a list contains only alphabet randomly with fixed length of input args """
        return random.choices(self._alphabet, k=length)

    def shuffle_list(self, list_captcha: list) -> None:
        """This Method take a list and shuffle the list randomly"""
        random.shuffle(list_captcha)


class ImageCaptcha(BaseImageCaptcha):
    def __init__(self, app: Flask = None,
                 RECAPTCHA_LENGTH: int,
                 RECAPTCHA_ENABLE: bool,
                 RECAPTCHA_LOG: bool ,
                 RECAPTCHA_INCLUDE_LETTERS: bool,
                 RECAPTCHA_INCLUDE_NUMERIC: bool ,
                 RECAPTCHA_INCLUDE_PUNCTUATION: bool, ):

        if app:
            if not isinstance(app, Flask):
                raise ex.NotFlaskObject(f'{app} object is not a flask instance!')
            self.init_app(app=app)
        else:
            ...


    def init_app(self, app: Flask):
        if not isinstance(app, Flask):
            raise ex.NotFlaskObject(f"object <{app}> is not a Flask Instance!")

    def generate(self):
        return self.__generate()

    def __generate(self):
        captchaCode = str(random.randint(self.RECAPTCHA_MIN, self.RECAPTCHA_MAX))
        imageCaptcha = self.IMAGER.generate(captchaCode)
        return base64.b64encode(imageCaptcha.getvalue()).decode('ascii')


    def validate(self):
        ...

    def __validate(self):
        pass
