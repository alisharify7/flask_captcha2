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
    """Master FlaskCaptcha Class
    this is master class, you should use object of this class for getting other captcha objects.
    
    Why we should first initializing this class? Because for creating other captcha objects we need
    to pass config every time we create them, but with this class we only pass config once to this
    class and this class will be hide all of that issues and (`Composite`) and give us a nice simple
    layer over all other captcha classes.

    `Example` initializing  class:
        ..code-block::python

                >> MasterCaptcha = FlaskCaptcha(app=app)

    `Example` Getting captcha object :

    ..code-block::python

                >> MasterCaptcha = FlaskCaptcha(app=app)
                >> google_captcha2 = MasterCaptcha.get_google_captcha_v2(..params)
    
    """

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

        `Example` config object:
            ..code-block::python
                
             {
                 "CAPTCHA_PRIVATE_KEY": "hish !",
                 "CAPTCHA_PUBLIC_KEY": "hish !",
                 'CAPTCHA_ENABLED': True,  # captcha status <True, False> 
                 "CAPTCHA_LOG": True, # show captcha logs in console
                 "CAPTCHA_LANGUAGE": "en" # captcha language
             }
                
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

    def get_google_captcha_v3(self, name: str, conf: dict = None, *args, **kwargs) -> FlaskCaptcha3:
        """this method return `FlaskCaptcha3` object.

        
        :param name: a unique name for captcha object. it is better to be a combination of captcha type and version
        :type name: str
        :param conf: a dictionary with config for captcha object
        :type conf: dict

        `Example` config object:
            ..code-block::python
                        
                 {
                     "CAPTCHA_PRIVATE_KEY": "hish !",
                     "CAPTCHA_PUBLIC_KEY": "hish !",
                     'CAPTCHA_ENABLED': True,  # captcha status <True, False> 
                     "CAPTCHA_SCORE": 0.5,  #google captcha version3 works with scores
                     "CAPTCHA_LOG": True  # show captcha requests and logs in terminal > stdout
                 }
        
        :return: an FlaskCaptcha3 object
        :rtype: FlaskCaptcha3
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
        """ `render` a captcha widget into html template.
        Use this method in templates for rendering captcha widgets in html tempaltes
        
        :param model_name: [Required] name of the captcha object (namespace)
        :type model_name: str
        :param css: [Optional] css of captcha element 
        :type css: str
        :param id: [Optional] id of captcha element 
        :type id: str
        :param dataset:[Optional] dataset of captcha element
        :type dataset: str
        :param event: [Optional] javascript inline events 
        :type event: str

        :return: captcha widget
        :rtype: Markup

        """
        return self.__render_captcha_in_template(*args, **kwargs)

    def __render_captcha_in_template(self, model_name: str, *args, **kwargs) -> Markup:
        """render a captcha (`Markup`) object.
        
        `Dont` Use this method directlly inside template !
        instead use `render_captcha` method for safely 
        rendering captcha widget inside html templates

        If the captcha name (namespace) was not exists
        this method will raise an exception.

        :param model_name: [Required] namespace of captcha
        :type model_name: str

        :return: captcha widget
        :rtype: Markup
        
        """
        if (captchaObject := self.__get_captcha_from_mapper(model_name)):
            return captchaObject.renderWidget(*args, **kwargs)
        else:
            raise exceptions.CaptchaNameNotExists(
                f"""model_name {model_name} was not set to any captcha object in app.\n
                available captcha names: {self.__get_all_available_captcha_names()}""")

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
