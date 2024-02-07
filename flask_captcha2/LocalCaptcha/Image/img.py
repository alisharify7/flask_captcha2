import os
import random
import base64
import string

# libs
from flask import Flask, session
from captcha.image import ImageCaptcha
from markupsafe import Markup

# flask-captcha2
from flask_captcha2 import excep as ex
from flask_captcha2.Logger import get_logger


class BaseImageCaptcha:
    ENABLE: bool = True
    LOG: bool = True
    LENGTH: int = 6 # length of captcha
    SESSION_KEY_NAME:str = 'flask-captcha2-image-captcha-answer'

    HEIGHT:int= 220
    WIDTH:int=180

    INCLUDE_LETTERS: bool = False
    INCLUDE_NUMERIC: bool = True
    INCLUDE_PUNCTUATION: bool = False

    _letters: str = string.ascii_lowercase
    _punctuations: str = string.punctuation
    _numbers: str= string.digits
    _imgGeneratorEngine :ImageCaptcha=None

    Logger = get_logger("Flask-Captcha2-ImageCaptcha")


    @property
    def LETTERS(self):
        """getter for letters"""
        return self._letters

    @LETTERS.setter
    def LETTERS(self, value:str):
        """setter for letters """
        if not isinstance(value, str):
            raise ValueError(f"letters {value} must be a string not a {type(value)}")
        else:
            self._letters = value


    @property
    def NUMBERS(self):
        return self._numbers


    @NUMBERS.setter
    def NUMBERS(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"numbers {value} must be a string not a {type(value)}")
        else:
            self._numbers = value


    @property
    def PUNCTUATIONS(self):
        return self._punctuations


    @PUNCTUATIONS.setter
    def PUNCTUATIONS(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"punctuation must be a string not a {type(value)}")
        else:
            self._punctuations = value



    def random_number(self, length: int) -> list:
        """return a list contains only numbers randomly with fixed length of input args """
        return random.choices(self.NUMBERS, k=length)

    def random_punctuation(self, length: int) -> list:
        """return a list contains only punctuation randomly with fixed length of input args """
        return random.choices(self.PUNCTUATIONS, k=length)

    def random_letters(self, length: int) -> list:
        """return a list contains only alphabet randomly with fixed length of input args """
        return random.choices(self.LETTERS, k=length)

    def shuffle_list(self, list_captcha: list) -> None:
        """This Method take a list and shuffle the list randomly"""
        random.shuffle(list_captcha)


class FlaskImageCaptcha(BaseImageCaptcha):
    def __init__(self, app: Flask, **kwargs):
        """
        :param:
             CAPTCHA_IMAGE_ENABLE: bool,
             CAPTCHA_IMAGE_LOG: bool ,

             CAPTCHA_IMAGE_CAPTCHA_LENGTH: int, # length of CAPTCHA code in image
             CAPTCHA_IMAGE_INCLUDE_LETTERS: bool,
             CAPTCHA_IMAGE_INCLUDE_NUMERIC: bool ,
             CAPTCHA_IMAGE_INCLUDE_PUNCTUATION: bool,
             CAPTCHA_IMAGE_HEIGHT: int,
             CAPTCHA_IMAGE_WIDTH: int,

             CAPTCHA_IMAGE_SESSION_KEY_NAME: str

             custom image captcha:
                 CAPTCHA_IMAGE_LETTERS:str
                 CAPTCHA_IMAGE_NUMBERS:str
                 CAPTCHA_IMAGE_PUNCTUATIONS:str
        """

        if app:
            if not isinstance(app, Flask):
                raise ex.NotFlaskApp(f'object {app} is not a flask instance!,')
            self.init_app(app=app)
        else:
            # object config
            self.LOG = kwargs.get("CAPTCHA_IMAGE_LOG")
            self.ENABLE = kwargs.get("CAPTCHA_IMAGE_ENABLE")

            self.LETTERS = kwargs.get("CAPTCHA_IMAGE_LETTERS")  # setter call
            self.NUMBERS = kwargs.get("CAPTCHA_IMAGE_NUMBERS")  # setter call
            self.PUNCTUATIONS = kwargs.get("CAPTCHA_IMAGE_PUNCTUATIONS")    # setter call

            # session config
            self.SESSION_KEY_NAME = kwargs.get("CAPTCHA_IMAGE_SESSION_KEY_NAME")

            # image configs
            self.INCLUDE_LETTERS = kwargs.get("CAPTCHA_IMAGE_INCLUDE_LETTERS")
            self.INCLUDE_NUMERIC = kwargs.get("CAPTCHA_IMAGE_INCLUDE_NUMERIC")
            self.INCLUDE_PUNCTUATION = kwargs.get("CAPTCHA_IMAGE_INCLUDE_PUNCTUATION")

            self.WIDTH = kwargs.get("CAPTCHA_IMAGE_WIDTH")
            self.HEIGHT = kwargs.get("CAPTCHA_IMAGE_HEIGHT")
            self.LENGTH = kwargs.get("CAPTCHA_IMAGE_CAPTCHA_LENGTH") # length of CAPTCHA code in image

            self._imgGeneratorEngine = ImageCaptcha(height=self.HEIGHT, width= self.WIDTH)

    def init_app(self, app: Flask):
        if not isinstance(app, Flask):
            raise ex.NotFlaskApp(f'object {app} is not a flask instance!,')

        self.__init__(
            app=None,
            CAPTCHA_IMAGE_LOG=app.config.get("CAPTCHA_IMAGE_LOG", self.LOG),
            CAPTCHA_IMAGE_ENABLE=app.config.get("CAPTCHA_IMAGE_ENABLE", self.ENABLE),
            CAPTCHA_IMAGE_LETTERS=app.config.get("CAPTCHA_IMAGE_LETTERS", self.LETTERS),
            CAPTCHA_IMAGE_NUMBERS=app.config.get("CAPTCHA_IMAGE_NUMBERS", self.NUMBERS),
            CAPTCHA_IMAGE_PUNCTUATIONS=app.config.get("CAPTCHA_IMAGE_PUNCTUATIONS", self.PUNCTUATIONS),
            CAPTCHA_IMAGE_SESSION_KEY_NAME=app.config.get("CAPTCHA_IMAGE_SESSION_KEY_NAME", self.SESSION_KEY_NAME),
            CAPTCHA_IMAGE_INCLUDE_LETTERS=app.config.get("CAPTCHA_IMAGE_INCLUDE_LETTERS", self.INCLUDE_LETTERS),
            CAPTCHA_IMAGE_INCLUDE_NUMERIC=app.config.get("CAPTCHA_IMAGE_INCLUDE_NUMERIC", self.INCLUDE_NUMERIC),
            CAPTCHA_IMAGE_INCLUDE_PUNCTUATION=app.config.get("CAPTCHA_IMAGE_INCLUDE_PUNCTUATION", self.INCLUDE_PUNCTUATION),
            CAPTCHA_IMAGE_WIDTH=app.config.get("CAPTCHA_IMAGE_WIDTH", self.WIDTH),
            CAPTCHA_IMAGE_HEIGHT=app.config.get("CAPTCHA_IMAGE_HEIGHT", self.HEIGHT),
            CAPTCHA_IMAGE_CAPTCHA_LENGTH=app.config.get("CAPTCHA_IMAGE_CAPTCHA_LENGTH", self.LENGTH)
        )


    def renderWidget(self, *args, **kwargs) -> Markup:
        """render captcha widget -> image in template"""
        return self.__generate(*args, **kwargs)

    def __generate(self, *args, **kwargs) -> Markup:
        """
        Generate image captcha with base on given args


        params:
                .. include_numbers: bool: True
                .. include_letters: bool: False
                .. include_punctuations: bool: False

        """

        numeric = kwargs.get("include_numbers", self.INCLUDE_NUMERIC)
        letters = kwargs.get("include_letters", self.INCLUDE_LETTERS)
        punctuation = kwargs.get("include_punctuations", self.INCLUDE_PUNCTUATION)

        # single mode captcha options
        captcha_raw_code = []
        if numeric and not letters and not punctuation:
            captcha_raw_code += self.random_number(length=self.LENGTH)
        if letters and not numeric and not punctuation:
            captcha_raw_code += self.random_letters(length=self.LENGTH)
        if punctuation and not numeric and not letters:
            captcha_raw_code += self.random_punctuation(length=self.LENGTH)

        if len(captcha_raw_code) == 0:  # mix captcha mode
            selected = {}
            if punctuation:
                selected["punctuation"] = self.random_punctuation
            if numeric:
                selected["numeric"] = self.random_number
            if letters:
                selected["letter"] = self.random_letters

            total = sum([letters, numeric, punctuation])
            each_round = self.LENGTH // total
            for each in selected:
                captcha_raw_code += (selected[each](length=each_round))
            captcha_raw_code += (self.random_letters(length=(self.LENGTH - len(captcha_raw_code))))
            self.shuffle_list(captcha_raw_code)

        captcha_raw_code = "".join(captcha_raw_code)
        image_data = self._imgGeneratorEngine.generate(captcha_raw_code)

        base64_captcha = base64.b64encode(image_data.getvalue()).decode("ascii")

        base64_captcha = f"data:image/png;base64, {base64_captcha}"

        self.Logger.info(f'Flask-Captcha2.ImageCaptcha.captcha generated:\tKey:{captcha_raw_code}')
        session[self.SESSION_KEY_NAME] = captcha_raw_code

        args = ""
        args += f"class=\"{kwargs.get('class')}\"\t" if kwargs.get('class') else ''
        args += f"id=\"{kwargs.get('id')}\"\t" if kwargs.get('id') else ''
        args += kwargs.get('dataset') + "\t" if kwargs.get('dataset') else ''
        args += f"style=\"{kwargs.get('style')}\"\t" if kwargs.get('style') else ''

        return Markup(f"<img src='{base64_captcha}' {args}>")



    def is_verify(self, CaptchaAnswer:str="") -> bool:
        print(session[self.SESSION_KEY_NAME] == CaptchaAnswer)
        if session.get(self.SESSION_KEY_NAME):
            if session.get(self.SESSION_KEY_NAME) == CaptchaAnswer:
                return True
        return False


    def __validate(self):
        pass
