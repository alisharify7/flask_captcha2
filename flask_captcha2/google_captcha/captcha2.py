"""
* flask_captcha2 OSS
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2023 - ali sharifi
* https://github.com/alisharify7/flask_captcha2
"""
import logging

# lib
import requests
from flask import request, Flask
from markupsafe import Markup

# flask-captcha2
from flask_captcha2 import excep as ex
from flask_captcha2.google_captcha.abstract_captcha import (
    GoogleCaptchaInterface,
    BaseGoogleCaptcha,
)
from flask_captcha2.mixins.logger_mixins import LoggerMixin


class BaseGoogleCaptcha2:
    """
    base config class fpr holding default configurations
    Base Google Captcha v2 class, contain default settings and properties
    """

    PUBLIC_KEY: str = ""
    PRIVATE_KEY: str = ""
    CAPTCHA_LOG: bool = True
    ENABLED: bool = False
    THEME: str = "light"
    TABINDEX: int = 0
    LANGUAGE: str = "en"
    TYPE: str = "image"
    SIZE: str = "normal"  # compact، normal، invisible
    GOOGLE_VERIFY_URL: str = "https://www.google.com/recaptcha/api/siteverify"


class GoogleCaptcha2(GoogleCaptchaInterface, BaseGoogleCaptcha, BaseGoogleCaptcha2, LoggerMixin):
    """Main Google Captcha version 2 captcha Class,

    `Don't` use this model directly, instead use
    FlaskCaptcha object for getting an instance
    of this model

    available config parameter:

    CAPTCHA_PRIVATE_KEY: "hish !"
    CAPTCHA_PUBLIC_KEY: "hish !"
    CAPTCHA_ENABLED: True  # captcha status <True, False>
    CAPTCHA_LOG: True # show captcha logs in console
    CAPTCHA_LANGUAGE: "en" # captcha language


    """

    def __init__(
        self,
        namespace: str,
        app: Flask = None,
        captcha_public_key: str = None,
        captcha_private_key: str = None,
        **kwargs,
    ) -> None:
        """
        if `app` object directly passed, then `init_app` method will be called.
        """
        if app and isinstance(app, Flask):  # app is passed read configs from app.config
            app.config["namespace"] = namespace
            self.init_app(app)
            self.logger = self.create_logger_object(logger_name=f"Logger-{namespace}")


        elif (
            captcha_public_key and captcha_private_key
        ):  # app is not passed read config from args passed to this method
            kwargs["captcha_private_key"] = captcha_private_key
            kwargs["captcha_public_key"] = captcha_public_key
            kwargs["namespace"] = namespace
            self.logger = self.create_logger_object(logger_name=f"Logger-{namespace}")
            self.set_config(kwargs)


    def init_app(self, app: Flask = None):
        """
        Initial setting of the object base on Flask-Application configuration
        """
        if not isinstance(app, Flask):
            raise ex.NotFlaskApp(f"{app} object is not a flask instance!")

        if not app.config.get("captcha_public_key", None) or not app.config.get(
            "captcha_public_key", None
        ):
            raise ValueError(
                "Flask-Captcha2.google_captcha.captcha2: Private and Public Keys are Required"
            )
        self.__init__(
            captcha_public_key=app.config.get("captcha_public_key", None),
            captcha_private_key=app.config.get("captcha_private_key", None),
            captcha_enabled=app.config.get("captcha_enabled", self.ENABLED),
            captcha_theme=app.config.get("captcha_theme", self.THEME),
            CAPTCHA_TYPE=app.config.get("captcha_type", self.TYPE),
            captcha_size=app.config.get("captcha_size", self.SIZE),
            captcha_language=app.config.get("captcha_language", self.LANGUAGE),
            captcha_tabindex=app.config.get("captcha_tabindex", self.TABINDEX),
            captcha_log=app.config.get("captcha_log", self.CAPTCHA_LOG),
            namespace=app.config.get("namespace", "google-captcha-v2"),
        )

    def set_config(self, conf: dict) -> None:
        """setting config base on config list passed in arg

        use this method for setting/refreshing configs for captcha object without passing flask main app
        """
        if not conf.get("captcha_public_key", False) or not conf.get(
            "captcha_private_key", False
        ):
            raise ValueError(
                "private_key and public_key are required for FlaskCaptcha2"
            )

        self.PUBLIC_KEY = conf.get("captcha_public_key")
        self.PRIVATE_KEY = conf.get("captcha_private_key")
        self.ENABLED = conf.get("captcha_enabled", self.ENABLED)
        self.THEME = conf.get("captcha_theme", self.THEME)
        self.TYPE = conf.get("captcha_type", self.TYPE)
        self.SIZE = conf.get("captcha_size", self.SIZE)
        self.LANGUAGE = conf.get("captcha_language", self.LANGUAGE)
        self.TABINDEX = conf.get("captcha_tabindex", self.TABINDEX)
        self.CAPTCHA_LOG = conf.get("captcha_log", self.CAPTCHA_LOG)
        self.NAMESPACE = conf.get("namespace", "google-captcha-v2")

    def is_verify(self) -> bool:
        """This Method Verify a Captcha v2 request

        no need to pass any value to this method, its grab `g-recaptcha-response`
        from POST data and send it to google server.

        response from Google is something like this
            ..code-block:: python

                - successful answer
                {
                    "success": true,
                    "challenge_ts": "2023-05-17T10:41:22Z",
                    "hostname": "127.0.0.1"
                }
                - failed answer
                {
                    "success": false,
                    "error-codes": [
                        "invalid-input-response"
                    ]
                }

        :return: `True` if the captcha verified successfully by google otherwise `False`
        :rtype: bool
        """
        if not self.ENABLED:
            return True

        data = {
            "secret": self.PRIVATE_KEY,
            "response": request.form.get("g-recaptcha-response", None),
        }
        response_google = requests.get(self.GOOGLE_VERIFY_URL, params=data)
        result = response_google.status_code == 200 and response_google.json()["success"]
        self.debug_log(f"google response: {response_google.json()}")
        return result

    def render_widget(self, *args, **kwargs) -> Markup:
        """render captcha widget

        :param id: html id of captcha widget
        :type id: str

        :param css_class: css class of captcha widget
        :type css_class: str

        :param inline_css: inline css style of captcha widget
        :type inline_css: str

        :param dataset: dataset of captcha widget
        :type dataset: str

        :param js_event: javascript inline event of captcha widget
        :type js_event: str

        :return: captcha widget
        :rtype: Markup
        """

        arg = ""
        # id
        arg += f"id=\"{kwargs.get('id')}\"\t" if kwargs.get("id") else ""
        # dataset
        arg += kwargs.get("dataset") + "\t" if kwargs.get("dataset") else ""
        # inline css style
        arg += (
            f"style=\"{kwargs.get('inline_css')}\"\t"
            if kwargs.get("inline_css")
            else ""
        )
        # js event
        arg += f"{kwargs.get('js_event', '')}"

        captcha_field = (
            f"""
        <script src='https://www.google.com/recaptcha/api.js'></script>
            <div class="g-recaptcha {kwargs.get('css_class', '')}" data-sitekey="{self.PUBLIC_KEY}"
                data-theme="{self.THEME}" data-lang="{self.LANGUAGE}" data-type="{self.TYPE}" data-size="{self.SIZE}"
                data-tabindex="{self.TABINDEX}" {arg}>
            </div>
        """
        ).strip()
        if self.ENABLED:
            return Markup(captcha_field)
        else:
            return Markup(" ")
