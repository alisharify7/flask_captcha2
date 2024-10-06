"""
 * flask_captcha2 OSS
 * author: github.com/alisharify7
 * email: alisharifyofficial@gmail.com
 * license: see LICENSE for more details.
 * Copyright (c) 2023 - ali sharifi
 * https://github.com/alisharify7/flask_captcha2
"""

# build in
import base64
import logging
import secrets
import string
from captcha.image import ImageCaptcha

# libs
from flask import Flask, session
from markupsafe import Markup
from random import SystemRandom

# flask-captcha2
from flask_captcha2 import excep as ex
from flask_captcha2.Logger import get_logger


class BaseImageCaptcha:
    """ Base default configuration class for image captcha """

    ENABLE: bool = True
    LOG: bool = True
    LENGTH: int = 6  # length of captcha
    SESSION_KEY_NAME: str = "flask-captcha2-image-captcha-answer"

    HEIGHT: int = 220
    WIDTH: int = 180

    INCLUDE_LETTERS: bool = False
    INCLUDE_NUMERIC: bool = True
    INCLUDE_PUNCTUATION: bool = False

    _letters: str = string.ascii_lowercase
    _punctuations: str = string.punctuation
    _numbers: str = string.digits
    _imgGeneratorEngine: ImageCaptcha = None

    # https://stackoverflow.com/questions/54672594/why-is-random-random-not-secure-in-python
    random = SystemRandom()  # https://docs.python.org/3/library/random.html
    Logger = get_logger(
        LogLevel=logging.DEBUG, logger_name="Flask-Captcha2-ImageCaptcha"
    )

    @property
    def LETTERS(self):
        """getter method for letters"""
        return self._letters

    @LETTERS.setter
    def LETTERS(self, value: str):
        """setter for letters"""
        if not isinstance(value, str):
            raise ValueError(
                f"letters {value} must be a string not a {type(value)}"
            )
        else:
            self._letters = value

    @property
    def NUMBERS(self):
        return self._numbers

    @NUMBERS.setter
    def NUMBERS(self, value: str):
        if not isinstance(value, str):
            raise ValueError(
                f"numbers {value} must be a string not a {type(value)}"
            )
        else:
            self._numbers = value

    @property
    def PUNCTUATIONS(self):
        return self._punctuations

    @PUNCTUATIONS.setter
    def PUNCTUATIONS(self, value: str):
        if not isinstance(value, str):
            raise ValueError(
                f"punctuation must be a string not a {type(value)}"
            )
        else:
            self._punctuations = value

    def random_number(self, length: int) -> list:
        """return a list contains only numbers randomly with fixed length of input args"""
        return [
            secrets.choice(self.NUMBERS) for i in range(length)
        ]  # replace random with secrets

    def random_punctuation(self, length: int) -> list:
        """return a list contains only punctuation randomly with fixed length of input args"""
        return [
            secrets.choice(self.PUNCTUATIONS) for i in range(length)
        ]  # replace random with secrets

    def random_letters(self, length: int) -> list:
        """return a list contains only alphabet randomly with fixed length of input args"""
        return [
            secrets.choice(self.LETTERS) for i in range(length)
        ]  # replace random with secrets

    def shuffle_list(self, list_captcha: list) -> None:
        """This Method take a list and shuffle the list randomly"""
        self.random.shuffle(list_captcha)

    def debug_log(self, message: str):
        """Print logs to stdout if CAPTCHA_IMAGE_LOG: bool  is set"""
        if self.LOG:
            self.Logger.debug(message)


class FlaskImageCaptcha(BaseImageCaptcha):
    def __init__(self, app: Flask, **kwargs):
        """
        constructor method.

        :param app: Flask application
        :type app: Flask

        this method can accept a flask app and extract configs from app.config it self,
        or you can pass the config directly using kwargs.

        :example of direct passing app:
            ..code-block:: python
                $> app.config.update(config_dict)
                $> FlaskImageCaptcha(app=app)
        
        :example passing config directly:
            ..code-block:: python
                $> FlaskImageCaptcha(CAPTCHA_IMAGE_ENABLE=True,  etc)


        Available config params:
         :param CAPTCHA_IMAGE_ENABLE: status of the captcha, is it enable or off
         :type CAPTCHA_IMAGE_ENABLE: bool
         
         :param CAPTCHA_IMAGE_LOG: log the messages in the `stdout` or not
         :type CAPTCHA_IMAGE_LOG: bool

         :param CAPTCHA_IMAGE_CAPTCHA_LENGTH: length of CAPTCHA code in image
         :type CAPTCHA_IMAGE_CAPTCHA_LENGTH: int
         
         :param CAPTCHA_IMAGE_INCLUDE_LETTERS: include the alphabet (a-z) in the captcha code or not
         :type CAPTCHA_IMAGE_INCLUDE_LETTERS: bool
         
         :param CAPTCHA_IMAGE_INCLUDE_NUMERIC: include the numbers in the captcha code
         :type CAPTCHA_IMAGE_INCLUDE_NUMERIC: bool
         
         :param CAPTCHA_IMAGE_INCLUDE_PUNCTUATION: include the punctuation in the captcha code or not
         :type CAPTCHA_IMAGE_INCLUDE_PUNCTUATION: bool
         
         :param CAPTCHA_IMAGE_HEIGHT: height of the captcha image
         ؛type CAPTCHA_IMAGE_HEIGHT: bool
         
         :param CAPTCHA_IMAGE_WIDTH: width of the captcha image 
         :type CAPTCHA_IMAGE_WIDTH: int

         :param CAPTCHA_IMAGE_SESSION_KEY_NAME: name of the captcha answer in the user session, [Optional],
         don't touch this if you don't know what it is
         :type CAPTCHA_IMAGE_SESSION_KEY_NAME: str

  
        """
        if app:
            if not isinstance(app, Flask):
                raise ex.NotFlaskApp(f"object {app} is not a flask instance!,")
            self.init_app(app=app)
        else:
            # object config
            self.LOG = kwargs.get("CAPTCHA_IMAGE_LOG")
            self.ENABLE = kwargs.get("CAPTCHA_IMAGE_ENABLE")

            self.LETTERS = kwargs.get("CAPTCHA_IMAGE_LETTERS")  # setter call
            self.NUMBERS = kwargs.get("CAPTCHA_IMAGE_NUMBERS")  # setter call
            self.PUNCTUATIONS = kwargs.get(
                "CAPTCHA_IMAGE_PUNCTUATIONS"
            )  # setter call

            # session config
            self.SESSION_KEY_NAME = kwargs.get(
                "CAPTCHA_IMAGE_SESSION_KEY_NAME"
            )

            # image configs
            self.INCLUDE_LETTERS = kwargs.get("CAPTCHA_IMAGE_INCLUDE_LETTERS")
            self.INCLUDE_NUMERIC = kwargs.get("CAPTCHA_IMAGE_INCLUDE_NUMERIC")
            self.INCLUDE_PUNCTUATION = kwargs.get(
                "CAPTCHA_IMAGE_INCLUDE_PUNCTUATION"
            )

            self.WIDTH = kwargs.get("CAPTCHA_IMAGE_WIDTH")
            self.HEIGHT = kwargs.get("CAPTCHA_IMAGE_HEIGHT")
            self.LENGTH = kwargs.get(
                "CAPTCHA_IMAGE_CAPTCHA_LENGTH"
            )  # length of CAPTCHA code in image

            self._imgGeneratorEngine = ImageCaptcha(
                height=self.HEIGHT, width=self.WIDTH
            )

    def init_app(self, app: Flask):
        """ 
            app init method, use this method when you using factory design and
            want to separate your extensions in  different file.
        """
        if not isinstance(app, Flask):
            raise ex.NotFlaskApp(f"object {app} is not a flask instance!,")

        self.__init__(
            app=None,
            CAPTCHA_IMAGE_LOG=app.config.get("CAPTCHA_IMAGE_LOG", self.LOG),
            CAPTCHA_IMAGE_ENABLE=app.config.get(
                "CAPTCHA_IMAGE_ENABLE", self.ENABLE
            ),
            CAPTCHA_IMAGE_LETTERS=app.config.get(
                "CAPTCHA_IMAGE_LETTERS", self.LETTERS
            ),
            CAPTCHA_IMAGE_NUMBERS=app.config.get(
                "CAPTCHA_IMAGE_NUMBERS", self.NUMBERS
            ),
            CAPTCHA_IMAGE_PUNCTUATIONS=app.config.get(
                "CAPTCHA_IMAGE_PUNCTUATIONS", self.PUNCTUATIONS
            ),
            CAPTCHA_IMAGE_SESSION_KEY_NAME=app.config.get(
                "CAPTCHA_IMAGE_SESSION_KEY_NAME", self.SESSION_KEY_NAME
            ),
            CAPTCHA_IMAGE_INCLUDE_LETTERS=app.config.get(
                "CAPTCHA_IMAGE_INCLUDE_LETTERS", self.INCLUDE_LETTERS
            ),
            CAPTCHA_IMAGE_INCLUDE_NUMERIC=app.config.get(
                "CAPTCHA_IMAGE_INCLUDE_NUMERIC", self.INCLUDE_NUMERIC
            ),
            CAPTCHA_IMAGE_INCLUDE_PUNCTUATION=app.config.get(
                "CAPTCHA_IMAGE_INCLUDE_PUNCTUATION", self.INCLUDE_PUNCTUATION
            ),
            CAPTCHA_IMAGE_WIDTH=app.config.get(
                "CAPTCHA_IMAGE_WIDTH", self.WIDTH
            ),
            CAPTCHA_IMAGE_HEIGHT=app.config.get(
                "CAPTCHA_IMAGE_HEIGHT", self.HEIGHT
            ),
            CAPTCHA_IMAGE_CAPTCHA_LENGTH=app.config.get(
                "CAPTCHA_IMAGE_CAPTCHA_LENGTH", self.LENGTH
            ),
        )

    def renderWidget(self, *args, **kwargs) -> Markup:
        """Render captcha widget image in template """
        return self.__generate(*args, **kwargs)

    def __generate(self, *args, **kwargs) -> Markup:
        """
        Generate image captcha with base on given args


        :param include_numbers: include the numbers (0-9) in the captcha or not 
        :type include_numbers: bool
        
        :param include_letters: include the alphabet (a-z) in the captcha or not
        :type include_letters: bool
        
        :param include_punctuations: include the punctuations (symbols) in the captcha or not
        :type include_punctuations: bool

        """
        if not self.ENABLE:
            return Markup(" ")

        numeric = kwargs.get("include_numbers", self.INCLUDE_NUMERIC)
        letters = kwargs.get("include_letters", self.INCLUDE_LETTERS)
        punctuation = kwargs.get(
            "include_punctuations", self.INCLUDE_PUNCTUATION
        )

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
            for each in selected: # fill the gap
                captcha_raw_code += selected[each](length=each_round)

            captcha_raw_code += self.random_letters(
                length=(self.LENGTH - len(captcha_raw_code))
            )  # fix gap (odd number)
            self.shuffle_list(captcha_raw_code)  # final shuffle

        captcha_raw_code = "".join(captcha_raw_code)
        image_data = self._imgGeneratorEngine.generate(captcha_raw_code)

        base64_captcha = base64.b64encode(image_data.getvalue()).decode(
            "ascii"
        )

        base64_captcha = f"data:image/png;base64, {base64_captcha}"

        self.debug_log(
            f"Flask-Captcha2.ImageCaptcha.captcha generated:\tKey:{captcha_raw_code}"
        )

        session[self.SESSION_KEY_NAME] = captcha_raw_code

        # external args
        args = ""
        args += (
            f"class=\"{kwargs.get('class')}\"\t" if kwargs.get("class") else ""
        )  # css class
        args += (
            f"id=\"{kwargs.get('id')}\"\t" if kwargs.get("id") else ""
        )  # id
        args += (
            kwargs.get("dataset") + "\t" if kwargs.get("dataset") else ""
        )  # dataset
        args += (
            f"style=\"{kwargs.get('style')}\"\t" if kwargs.get("style") else ""
        )  # style
        args += f"{kwargs.get('event', '')}"  # js event

        return Markup(f"<img src='{base64_captcha}' {args}>")

    def is_verify(self, captcha_answer: str = "") -> bool:
        """Verify the answer of the image captcha
        
        :param captcha_answer: answer that user type enter.
        :type captcha_answer: str

        :return: True or False
        :rtype: bool
        """
        if not self.ENABLE:
            return True

        if session.get(self.SESSION_KEY_NAME, False):
            if session.get(self.SESSION_KEY_NAME) == captcha_answer:
                session.pop(self.SESSION_KEY_NAME)
                return True
            session.pop(self.SESSION_KEY_NAME)
        return False
