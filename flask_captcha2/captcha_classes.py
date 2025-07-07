"""
* flask_captcha2 OSS
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2023 - ali sharifi
* https://github.com/alisharify7/flask_captcha2
"""

# build in
import logging
import typing

# lib
from flask import Flask
from markupsafe import Markup

# flask-captcha2
from . import excep as exceptions
from .google_captcha.captcha2 import GoogleCaptcha2
from .google_captcha.captcha3 import GoogleCaptcha3
from .local_captcha.image import SessionImageCaptcha
from .mixins.logger_mixins import LoggerMixin


class FlaskCaptcha(LoggerMixin):
    """Master FlaskCaptcha Class
    this is master class, you should use object of this class for getting other captcha objects.

    Why we should first initializing this class? Because for creating other captcha objects we need
    to pass config every time we create them, but with this class we only pass config once to this
    class and this class will be hide all of that issues and (`Composite`) and give us a nice simple
    layer over all other captcha classes.

    `Example` initializing  class:
        ..code-block::python

            >>> MasterCaptcha = FlaskCaptcha(app=app)

    `Example` Getting captcha object :

    ..code-block::python

            >>> MasterCaptcha = FlaskCaptcha(app=app)
            >>> google_captcha2 = MasterCaptcha.get_google_captcha_v2(..params)

    """

    CAPTCHA_TYPES = [
        "google-captcha-v2",
        "google-captcha-v3",
        "local-session-captcha-image",
    ]

    def __init__(self, app: Flask) -> None:
        """Constructor function
        :param app: flask application object
        :type app: Flask

        :return: None
        :rtype: None
        """
        if not app or not isinstance(app, Flask):
            raise ValueError(
                "Flask App is required. please provide flask app like FlaskCaptcha(app=app)"
            )

        @app.context_processor
        def app_context_processor():
            ctx = {"captcha": self}
            return ctx


        self.CAPTCHA_OBJECT_MAPPER_KEY_NAME = "captcha_object_mapper"
        self.DEBUG = app.debug
        self.FLASK_APP = app
        self.logger = self.create_logger_object(logger_level=logging.INFO, logger_name="FlaskCaptcha-Manager")
        app.config[self.CAPTCHA_OBJECT_MAPPER_KEY_NAME] = dict()



    @classmethod
    def create(cls, captcha_type: str, *args, **kwargs):
        # Factory method for creating captcha object manager
        if type not in cls.CAPTCHA_TYPES:
            raise RuntimeError("invalid type, type must be one of ")

        match captcha_type:
            case "google-captcha-v2":
                return cls.generate_google_captcha_v2(*args, **kwargs)
            case "google-captcha-v3":
                return cls.generate_google_captcha_v3(*args, **kwargs)
            case "local-captcha-image":
                return cls.generate_session_image_captcha(*args, **kwargs)
            case _:
                raise RuntimeError("invalid captcha type: {}".format(captcha_type))

    def generate_google_captcha_v2(
        self,
        namespace: str,
        conf: typing.Union[typing.Dict[str, str], None] = None,
        *args,
        **kwargs,
    ):
        """this method return `GoogleCaptcha2` object

        instead of direct using, use this method for generating a captcha version2 object
        :param namespace: a unique name for captcha object. it is better to be a combination of captcha type and version
        :type namespace: str
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

        if not namespace:
            raise ValueError("captcha should have a namespace!")
        if self.__is_namespace_exists(namespace=namespace):
            raise ValueError(f"duplicated captcha namespace! {self.__get_all_captcha_namespaces()}")

        if conf and isinstance(conf, dict):  # custom config is passed
            captcha = GoogleCaptcha2(namespace=namespace, **conf)
        else:
            captcha = GoogleCaptcha2(namespace=namespace, app=self.FLASK_APP)
        self.logger.warning(f"google captcha v2 with namespace={namespace} created.")
        self.__set_captcha_object(namespace=namespace, captcha_object=captcha)
        return self.__get_captcha_object(namespace=namespace)

    def generate_google_captcha_v3(
        self,
        namespace: str,
        conf: typing.Union[typing.Dict[str, str], None] = None,
        *args,
        **kwargs,
    ):
        """this method return `FlaskCaptcha3` object.


        :param namespace: a unique name for captcha object. it is better to be a combination of captcha type and version
        :type namespace: str
        :param conf: a dictionary with config for captcha object
        :type conf: dict

        `Example` config object:
            ..code-block::python

                 {
                     "captcha_private_key": "hish !",
                     "captcha_public_key": "hish !",
                     'captcha_enabled': True,  # captcha status <True, False>
                     "captcha_score": 0.5,  #google captcha version3 works with scores
                     "captcha_log": True  # show captcha requests and logs in terminal > stdout
                 }

        :return: an FlaskCaptcha3 object
        :rtype: FlaskCaptcha3
        """
        if not namespace:
            raise ValueError("captcha should have a name!")
        if self.__is_namespace_exists(namespace=namespace):
            raise ValueError("duplicated captcha name!")

        if conf and isinstance(conf, dict):  # custom config is passed
            captcha = GoogleCaptcha3(namespace=namespace, **conf)
        else:
            captcha = GoogleCaptcha3(namespace=namespace, app=self.FLASK_APP)

        self.logger.warning(f"google captcha v3 with namespace={namespace} created.")
        self.__set_captcha_object(namespace=namespace, captcha_object=captcha)
        return self.__get_captcha_object(namespace=namespace)

    def generate_session_image_captcha(
        self,
        namespace: str,
        conf: typing.Union[typing.Dict[str, str], None] = None,
        *args,
        **kwargs,
    ):
        """this method return `SessionImageCaptcha` object.


        :param namespace: a unique name for captcha object. it is better to be a combination of captcha type and version
        :type namespace: str
        :param conf: a dictionary with config for captcha object
        :type conf: dict

        `Example` config object:
            ..code-block::python

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

        :return: an FlaskCaptcha3 object
        :rtype: FlaskCaptcha3
        """
        if not namespace:
            raise ValueError("captcha should have a name!")
        if not self.__is_namespace_exists(namespace=namespace):
            raise ValueError("duplicated captcha name!")

        if conf and isinstance(conf, dict):  # custom config is passed
            captcha = SessionImageCaptcha(**conf, NAMESPACE=namespace)
        else:
            captcha = SessionImageCaptcha(app=self.FLASK_APP, NAMESPACE=namespace)

        self.__set_captcha_object(namespace=namespace, captcha_object=captcha)
        return self.__get_captcha_object(namespace=namespace)

    def render_captcha(self, *args, **kwargs) -> str:
        """`render` a captcha widget into html template.
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

    def __render_captcha_in_template(self, namespace: str, *args, **kwargs) -> Markup:
        """render a captcha (`Markup`) object.

        `Don't` Use this method directly inside template !
        instead use `render_captcha` method for safely
        rendering captcha widget inside html templates

        If the captcha name (namespace) was not exists
        this method will raise an exception.

        :param model_name: [Required] namespace of captcha
        :type model_name: str

        :return: captcha widget
        :rtype: Markup

        """
        if captcha_object := self.__get_captcha_object(namespace=namespace):
            return captcha_object.render_widget(*args, **kwargs)
        else:
            raise exceptions.CaptchaNameNotExists(
                f"""namespace {namespace} was not set to any captcha object in app.\n
                available captcha namespaces: {self.__get_all_captcha_namespaces()}"""
            )

    def __is_namespace_exists(self, namespace: str) -> bool:
        """check a captcha name (NameSpace) is not duplicated.

        :param name: name of captcha
        :type name: str

        :return: `False` if captcha name already exists, otherwise `True`
        :rtype: bool
        """
        return namespace in self.FLASK_APP.config[self.CAPTCHA_OBJECT_MAPPER_KEY_NAME]


    def __set_captcha_object(self, namespace: str, captcha_object: object) -> bool:
        """Set a captcha object with the given name (Namespace) in captcha mapper repo.

        This method saves (set) a captcha with the given name in
        captcha mapper repo.

        :param name: name of captcha object
        :type name: str

        :param captcha_object: captcha object
        :type captcha_object: object

        :return: `True` if captcha is set correctly in mapper, otherwise `False`
        """
        try:
            self.FLASK_APP.config[self.CAPTCHA_OBJECT_MAPPER_KEY_NAME][
                namespace
            ] = captcha_object
        except Exception as e:
            return False
        return True

    def __get_captcha_object(self, namespace: str) -> object:
        """getting captcha object from mapper repo.
        This method returns a CAPTCHA object with the given name
        (Namespace) That is registered in app.

        if the captcha name does not exist this method raises an exception

        :param name: name of captcha object
        :type name: str

        :return: object of captcha
        :rtype: object

        """
        if namespace in self.FLASK_APP.config[self.CAPTCHA_OBJECT_MAPPER_KEY_NAME]:
            return self.FLASK_APP.config[self.CAPTCHA_OBJECT_MAPPER_KEY_NAME][namespace]
        else:
            raise exceptions.CaptchaNameNotExists(
                f"invalid namespace. {namespace} was not set to any captcha object.\navailable namesspaces:{self.__get_all_captcha_namespaces()}"
            )

    def __get_all_captcha_namespaces(self) -> typing.List[str]:
        """return all registered NameSpaces.
        This method returns all CAPTCHA names that are registered in the app.config.

        :return: list of namespaces of all captcha objects thatare  registered in the app
        :rtype: List
        """
        return list(
            self.FLASK_APP.config.get(self.CAPTCHA_OBJECT_MAPPER_KEY_NAME, {}).keys()
        )

    def __str__(self) -> str:
        return f"<FlaskCaptcha MasterClass {self.FLASK_APP} >"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(app={self.FLASK_APP})"
