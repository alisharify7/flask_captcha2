"""
 * flask_captcha2 OSS
 * main import entrypoint
 * author: github.com/alisharify7
 * email: alisharifyofficial@gmail.com
 * license: see LICENSE for more details.
 * Copyright (c) 2023 - ali sharifi
 * https://github.com/alisharify7/flask_captcha2
"""

# build in
import json
import logging

# lib
import requests
from flask import request, Flask
from markupsafe import Markup

# flask-captcha2
from flask_captcha2 import excep as ex
from flask_captcha2.Logger import get_logger
from .utils import CommonCaptchaUtils


class BaseCaptcha2(CommonCaptchaUtils):
    """base config class fpr holding default configurations
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

    Logger = get_logger(
        LogLevel=logging.DEBUG, CaptchaName="Google-Captcha-v2"
    )


class FlaskCaptcha2(BaseCaptcha2):
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
        app: Flask = None,
        CAPTCHA_PUBLIC_KEY: str = None,
        CAPTCHA_PRIVATE_KEY: str = None,
        **kwargs,
    ) -> None:
        """
        if `app` object directly passed, then `init_app` method will be called.
        """
        if app and isinstance(
            app, Flask
        ):  # app is passed read configs from app.config
            self.init_app(app)

        elif (
            CAPTCHA_PUBLIC_KEY and CAPTCHA_PRIVATE_KEY
        ):  # app is not passed read config from args passed to this method
            kwargs["CAPTCHA_PRIVATE_KEY"] = CAPTCHA_PRIVATE_KEY
            kwargs["CAPTCHA_PUBLIC_KEY"] = CAPTCHA_PUBLIC_KEY
            self.set_config(kwargs)

    def init_app(self, app: Flask = None):
        """
        Initial setting of the object base on Flask-Application configuration
        """
        if not isinstance(app, Flask):
            raise ex.NotFlaskApp(f"{app} object is not a flask instance!")

        if not app.config.get(
            "CAPTCHA_PUBLIC_KEY", None
        ) or not app.config.get("CAPTCHA_PRIVATE_KEY", None):
            raise ValueError(
                "Flask-Captcha2.GoogleCaptcha.captcha2: Private and Public Keys are Required"
            )

        self.__init__(
            CAPTCHA_PUBLIC_KEY=app.config.get("CAPTCHA_PUBLIC_KEY", None),
            CAPTCHA_PRIVATE_KEY=app.config.get("CAPTCHA_PRIVATE_KEY", None),
            CAPTCHA_ENABLED=app.config.get("CAPTCHA_ENABLED", self.ENABLED),
            CAPTCHA_THEME=app.config.get("CAPTCHA_THEME", self.THEME),
            CAPTCHA_TYPE=app.config.get("CAPTCHA_TYPE", self.TYPE),
            CAPTCHA_SIZE=app.config.get("CAPTCHA_SIZE", self.SIZE),
            CAPTCHA_LANGUAGE=app.config.get("CAPTCHA_LANGUAGE", self.LANGUAGE),
            CAPTCHA_TABINDEX=app.config.get("CAPTCHA_TABINDEX", self.TABINDEX),
            CAPTCHA_LOG=app.config.get("CAPTCHA_LOG", self.CAPTCHA_LOG),
        )

    def set_config(self, conf_list: dict) -> None:
        """setting config base on config list passed in arg

        use this method for setting/refreshing configs for captcha object without passing flask main app
        """
        if not conf_list.get("CAPTCHA_PUBLIC_KEY", False) or not conf_list.get(
            "CAPTCHA_PRIVATE_KEY", False
        ):
            raise ValueError(
                "private_key and public_key are required for FlaskCaptcha2"
            )

        self.PUBLIC_KEY = conf_list.get("CAPTCHA_PUBLIC_KEY")
        self.PRIVATE_KEY = conf_list.get("CAPTCHA_PRIVATE_KEY")
        self.ENABLED = conf_list.get("CAPTCHA_ENABLED", self.ENABLED)
        self.THEME = conf_list.get("CAPTCHA_THEME", self.THEME)
        self.TYPE = conf_list.get("CAPTCHA_TYPE", self.TYPE)
        self.SIZE = conf_list.get("CAPTCHA_SIZE", self.SIZE)
        self.LANGUAGE = conf_list.get("CAPTCHA_LANGUAGE", self.LANGUAGE)
        self.TABINDEX = conf_list.get("CAPTCHA_TABINDEX", self.TABINDEX)
        self.CAPTCHA_LOG = conf_list.get("CAPTCHA_LOG", self.CAPTCHA_LOG)

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
        else:
            data = {
                "secret": self.PRIVATE_KEY,
                "response": request.form.get("g-recaptcha-response", None),
            }

            responseGoogle = requests.get(self.GOOGLE_VERIFY_URL, params=data)

            if self.CAPTCHA_LOG:
                self.debug_log(f"SEND REQUEST TO {self.GOOGLE_VERIFY_URL}")
                self.debug_log(
                    f"GOOGLE RESPONSE:\n {json.dumps(responseGoogle.json(), indent=4)}"
                )

            if responseGoogle.status_code == 200:
                return responseGoogle.json()["success"]
            else:
                return False

    def renderWidget(self, *args, **kwargs) -> Markup:
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

        CaptchaField = (
            f"""
        <script src='https://www.google.com/recaptcha/api.js'></script>
            <div class="g-recaptcha {kwargs.get('css_class', '')}" data-sitekey="{self.PUBLIC_KEY}"
                data-theme="{self.THEME}" data-lang="{self.LANGUAGE}" data-type="{self.TYPE}" data-size="{self.SIZE}"
                data-tabindex="{self.TABINDEX}" {arg}>
            </div>
        """
        ).strip()
        if self.ENABLED:
            return Markup(CaptchaField)
        else:
            return Markup(" ")
