# build in
import logging
# lib
from flask import Flask
from markupsafe import Markup

from . import excep as exceptions
# flask-captcha2
from .GoogleCaptcha.captcha2 import FlaskCaptcha2
from .GoogleCaptcha.captcha3 import FlaskCaptcha3
from .Logger import get_logger


class FlaskCaptcha:
    """Master FlaskCaptcha Class"""

    def __init__(self, app: Flask) -> None:
        """Constructor function
        :param app: flask application object
        :type app: Flask

        :retrun: None
        :rtype: None
        """
        if not app or not isinstance(app, Flask):
            raise ValueError("Flask App is required. please provide flask app like FlaskCaptcha(app=app)")

        @app.context_processor
        def app_context_processor():
            ctx = {
                "captcha": self
            }
            return ctx

        app.config["captcha_object_mapper"] = {}  # keep all captcha object : key:value -> name:object
        self.__debug = app.debug
        self.__app = app
        self.__logger = get_logger(LogLevel=logging.INFO, CaptchaName="Flask-Captcha2-Master")

    def __print_log(self, message: str):
        """print a log message"""
        self.__logger.info(message)

    def get_google_captcha_v2(self, name: str, conf: dict = None, *args, **kwargs) -> FlaskCaptcha2:
        """this method return `FlaskCaptcha2` object

        :parama name: a unique name for captcha object. it is better to be a combination of captcha type and version
        :type name: str
        :param conf: a dictionary with config for captcha object
        :type conf: dict
        
        :return: an FlaskCaptcha2 object
        :rtype: FlaskCaptcha2
        
        """

        if not name:
            raise ValueError("captcha should have a name!")
        if not self.__check_duplicate_captcha_name(name):
            raise ValueError("duplicated captcha name!")

        if conf and isinstance(conf, dict):  # custom config is passed
            captcha = FlaskCaptcha2(**conf)
        else:
            captcha = FlaskCaptcha2(app=self.__app)

        self.__set_captcha_mapper(name=name, captchaObject=captcha)
        self.__print_log(f"Google-Captcha-version-2 created successfully,\n\tcaptcha-name:{name}")
        return self.__get_captcha_from_mapper(name=name)

    def getGoogleCaptcha3(self, name: str, conf: dict = None, *args, **kwargs) -> FlaskCaptcha3:
        """return a flask captcha object for google captcha version 3

        Args:
        name:str: a unique name for captcha object. it is better to be a combination of captcha type and version
        
        Returns:
            captchaObject: FlaskCaptcha2: an FlaskCaptcha3 object
        """
        if not name:
            raise ValueError("captcha should have a name!")
        if not self.__check_duplicate_captcha_name(name):
            raise ValueError("duplicated captcha name!")

        if conf and isinstance(conf, dict):  # custom config is passed
            captcha = FlaskCaptcha3(**conf)
        else:
            captcha = FlaskCaptcha3(app=self.__app)

        self.__set_captcha_mapper(name=name, captchaObject=captcha)
        self.__print_log(f"Google-Captcha-version-3 created successfully,\n\tcaptcha-name:{name}")
        return self.__get_captcha_from_mapper(name=name)

    def render_captcha(self, *args, **kwargs):
        """
        Use this method in templates for rendering captcha widgets in your template
        
        Args: 
            model_name: str: required, name of the captcha object
            
            css: str: css of captcha element [Optional]
            id:str: id of captcha element [Optional]
            dataset: str: dataset of captcha element [Optional]
            event: str: js events [Optional]

        Returns: 
            Captcha: Markup: captcha widget

        """
        return self.__render_captcha_in_template(*args, **kwargs)

    def __render_captcha_in_template(self, model_name: str, *args, **kwargs) -> Markup:
        """render a captcha base on captcha name in param
        this method check if captcha name exists in app.config['captcha_object_mapper']
        then its call .renderWidget method in captcha object
        
        Args: 
            model_name: str: required, name of the captcha object
            
            css: str: css of captcha element [Optional]
            id:str: id of captcha element [Optional]
            dataset: str: dataset of captcha element [Optional]
            javascriptEvents: str: js events [Optional]

        Returns: 
            Captcha: Markup: captcha widget
        
        if the captcha name was not exists this method Raise an exception

        """
        if (captchaObject := self.__get_captcha_from_mapper(model_name)):
            return captchaObject.renderWidget(*args, **kwargs)
        else:
            raise exceptions.CaptchaNameNotExists(
                f"invalid model name. {model_name} was not set to any captcha object.\navailable captcha names:{self.__get_all_available_captcha_names()}")

    def __check_duplicate_captcha_name(self, name: str) -> bool:
        """check a captcha object name is not duplicated in app
        
        Args:
            name: str: name of captcha
        
        Returns:
            Bool `False` if captcha name is already exists, otherwise `True` 
        """
        if name in self.__app.config["captcha_object_mapper"]:
            return False
        return True

    def __set_captcha_mapper(self, name: str, captchaObject) -> bool:
        """This Method get a captcha and name of it and save it in app.config[captcha_object_mapper] 
        
        Args:
            name:str: name of captcha object
            captchaObject: class object : captcha object

        Returns:
            bool: `True` if captcha set in config successfully, `False` otherwise
        """
        try:
            self.__app.config["captcha_object_mapper"][name] = captchaObject
        except Exception as e:
            return False
        return True

    def __get_captcha_from_mapper(self, name: str) -> object:
        """
        This Method get a captcha name and return that captcha objects from app.config
        
        Args:
            name:str: name of captcha object
        
        Returns:
            captcha: captcha object: object of captcha

        if the captcha name was not exists this method Raise an exception
        """
        if name in self.__app.config["captcha_object_mapper"]:
            return self.__app.config["captcha_object_mapper"][name]
        else:
            raise exceptions.CaptchaNameNotExists(
                f"invalid model name. {name} was not set to any captcha object.\navailable captcha names:{self.__get_all_available_captcha_names()}")

    def __get_all_available_captcha_names(self) -> list:
        """
        This method return all captcha names that registered in app.config

        Args:
            None

        Returns:
            list: list: a list of name of captcha objects that registered in app 
        """
        return list(self.__app.config.get('captcha_object_mapper').keys())
