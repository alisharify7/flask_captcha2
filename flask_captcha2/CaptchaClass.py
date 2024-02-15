# build in
import logging

# lib
from flask import Flask

# flask-captcha2
from .GoogleCaptcha.captcha2 import FlaskCaptcha2
from .GoogleCaptcha.captcha3 import FlaskCaptcha3
from .LocalCaptcha.Image import FlaskImageCaptcha
from .Logger import get_logger


class FlaskCaptcha:

    def __init__(self, app: Flask):
        """Constructor function

        this function set captcha key in  app.context_processor for getting captcha object acros the application templates
        and also initiate the captcha_object_mapper storage in app.config
        """
        if not app or not isinstance(app, Flask):
            raise ValueError("Flask App is required. please provide app like FlaskCaptcha(app=app)")

        @app.context_processor
        def app_context_processor():
            ctx = {
                "captcha": self
            }
            return ctx

        app.config["captcha_object_mapper"] = {}  # keep all captcha object and names
        self.__debug = app.debug
        self.__app = app
        self.__logger = get_logger(LogLevel=logging.INFO, CaptchaName="Flask-Captcha2-Master")

    def print_log(self, message:str):
        self.__logger.info(message)

    def getGoogleCaptcha2(self, name: str, *args, **kwargs) -> FlaskCaptcha2:
        """return a flask captcha object for google captcha version 2

        args:
            . name:str: a unique name for captcha object. it is better to be a combination of captcha type and version
        """
        if not name:
            raise ValueError("captcha should have a name!")
        if not self.__check_duplicate_captcha_name(name):
            raise ValueError("duplicated captcha name!")

        captcha = FlaskCaptcha2(app=self.__app)
        self.__set_captcha_mapper(name=name, captchaObject=captcha)
        self.print_log(f"Google-Captcha-version-2 created successfully,\n\tcaptcha-name{name}")
        return self.__get_captcha_from_mapper(name=name)

    def getGoogleCaptcha3(self, name: str, *args, **kwargs) -> FlaskCaptcha3:
        """return a flask captcha object for google captcha version 3

        args:
            . name:str: a unique name for captcha object. it is better to be a combination of captcha type and version
        """
        if not name:
            raise ValueError("captcha should have a name!")
        if not self.__check_duplicate_captcha_name(name):
            raise ValueError("duplicated captcha name!")

        captcha = FlaskCaptcha3(app=self.__app)
        self.__set_captcha_mapper(name=name, captchaObject=captcha)
        self.print_log(f"Google-Captcha-version-3 created successfully,\n\tcaptcha-name{name}")
        return self.__get_captcha_from_mapper(name=name)

    def getLocalImageCaptcha(self, name: str, *args, **kwargs) -> FlaskImageCaptcha:
        if not name:
            raise ValueError("captcha should have a name!")
        if not self.__check_duplicate_captcha_name(name):
            raise ValueError("duplicated captcha name!")

        captcha = FlaskImageCaptcha(app=self.__app)
        self.__set_captcha_mapper(name=name, captchaObject=captcha)
        self.print_log(f"local-image-captcha created successfully,\n\tcaptcha-name{name}")
        return self.__get_captcha_from_mapper(name=name)

    def render_captcha(self, *args, **kwargs):
        """Use this method in templates for rendering captcha widgets in your template"""
        return self.__render_captcha_in_template(*args, **kwargs)

    def __render_captcha_in_template(self, model_name: str, *args, **kwargs):
        """render a captcha base on captcha name in param"""
        if (captchaObject := self.__get_captcha_from_mapper(model_name)):
            return captchaObject.renderWidget(*args, **kwargs)
        else:
            raise ValueError(
                f"invalid model name. {model_name} was not set to any captcha object.\navailable captcha names:{self.__get_all_available_captcha_names()}")

    def __check_duplicate_captcha_name(self, name: str):
        """check a captcha object name is not duplicated in app"""
        if name in self.__app.config["captcha_object_mapper"]:
            return False
        return True

    def __set_captcha_mapper(self, name: str, captchaObject) -> bool:
        """This Method get a captcha object and name and save it in app.config[captcha_object_mapper] """
        try:
            self.__app.config["captcha_object_mapper"][name] = captchaObject
        except Exception as e:
            return False
        return True

    def __get_captcha_from_mapper(self, name: str):
        """This Method get a captcha name and return that captcha objects from app.config"""
        if name in self.__app.config["captcha_object_mapper"]:
            return self.__app.config["captcha_object_mapper"][name]
        return False

    def __get_all_available_captcha_names(self):
        """This method return all captcha names that registered"""
        return list(self.__app.config.get('captcha_object_mapper').keys())
