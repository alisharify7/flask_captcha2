"""
* flask_captcha2 OSS
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
from flask_captcha2.logger import get_logger
from flask_captcha2.google_captcha.utils import CommonCaptchaUtils
from flask_captcha2.google_captcha.abstract_captcha import (
    GoogleCaptchaInterface,
    BaseGoogleCaptcha,
)


class BaseGoogleCaptcha3(CommonCaptchaUtils):
    """base config class fpr holding default configurations
    Base Google Captcha v3 class, contain default settings and properties
    """

    PUBLIC_KEY: str = ""
    PRIVATE_KEY: str = ""
    ENABLED: bool = False
    SCORE: float = 0.5
    MINIMUM_SCORE: float = 0.5  # default minimum score
    CAPTCHA_LOG: bool = True
    GOOGLE_VERIFY_URL: str = "https://www.google.com/recaptcha/api/siteverify"

    Logger = get_logger(log_level=logging.DEBUG, logger_name="Google-Captcha-v3")

    HIDE_CAPTCHA_WIDGET_CSS = "<style>.grecaptcha-badge {visibility: hidden;}</style>"


class GoogleCaptcha3(GoogleCaptchaInterface, BaseGoogleCaptcha, BaseGoogleCaptcha3):
    """Main Google Captcha version 3 captcha Class,

    `Don't` use this model directly, instead use
    FlaskCaptcha object for getting an instance
    of this model

    available config parameter:

    CAPTCHA_PUBLIC_KEY <str:: public Key from googleDevelopers panel>
    CAPTCHA_PRIVATE_KEY <str:: public Key from googleDevelopers panel>
    CAPTCHA_SCORE <Float:: score for verify each request between 0.5 - 1>
    CAPTCHA_ENABLED <Boolean::captcha status>
    CAPTCHA_LOG <Boolean:: Show each Request Log in terminal>


    """

    def __init__(
        self,
        app: Flask = None,
        CAPTCHA_PUBLIC_KEY: str = None,
        CAPTCHA_PRIVATE_KEY: str = None,
        **kwargs,
    ) -> None:
        if app and isinstance(app, Flask):  # app is passed read configs from app.config
            self.init_app(app)

        elif (
            CAPTCHA_PRIVATE_KEY and CAPTCHA_PUBLIC_KEY
        ):  # app is not passed read config from args passed to this method
            kwargs["CAPTCHA_PRIVATE_KEY"] = CAPTCHA_PRIVATE_KEY
            kwargs["CAPTCHA_PUBLIC_KEY"] = CAPTCHA_PUBLIC_KEY
            self.set_config(kwargs)

    def init_app(self, app: Flask = None) -> None:
        if not isinstance(app, Flask):
            raise ex.NotFlaskApp(f"{app} object is not a flask instance!")

        if not app.config.get("CAPTCHA_PUBLIC_KEY", None) or not app.config.get(
            "CAPTCHA_PRIVATE_KEY", None
        ):
            raise ValueError(
                "Flask-Captcha2.google_captcha.captcha3: Private and Public Keys are Required"
            )

        self.__init__(
            CAPTCHA_PUBLIC_KEY=app.config.get("CAPTCHA_PUBLIC_KEY", None),
            CAPTCHA_PRIVATE_KEY=app.config.get("CAPTCHA_PRIVATE_KEY", None),
            CAPTCHA_ENABLED=app.config.get("CAPTCHA_ENABLED", self.ENABLED),
            CAPTCHA_SCORE=app.config.get("CAPTCHA_SCORE", self.SCORE),
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
                "private_key and public_key are required for FlaskCaptcha3"
            )

        self.PUBLIC_KEY = conf_list.get("CAPTCHA_PUBLIC_KEY")
        self.PRIVATE_KEY = conf_list.get("CAPTCHA_PRIVATE_KEY")
        self.ENABLED = conf_list.get("CAPTCHA_ENABLED", self.ENABLED)
        self.CAPTCHA_LOG = conf_list.get("CAPTCHA_LOG", self.CAPTCHA_LOG)
        try:
            self.SCORE = (
                self.MINIMUM_SCORE
                if int(conf_list.get("CAPTCHA_SCORE", self.SCORE)) < self.MINIMUM_SCORE
                else int(conf_list.get("CAPTCHA_SCORE", self.SCORE))
            )
        except ValueError:
            self.SCORE = self.MINIMUM_SCORE

    def is_verify(self) -> bool:
        """This Method Verify a Captcha v2 request

        no need to pass any value to this method, its grab `g-recaptcha-response`
        from POST data and send it to google server.

        example google response
        ..code-block::python

            {
                 'success': True,
                 'challenge_ts': '2023-04-04T07:39:45Z',
                 'hostname': '127.0.0.1',
                 'score': 0.9,
                 'action': 'submit'
            }

        :return: `True` if the captcha verified successfully by google otherwise `False`
        :rtype: bool
        """

        if not self.ENABLED:
            return True
        else:
            response = request.form.get("g-recaptcha-response", None)

            responseGoogle = requests.post(
                f"{self.GOOGLE_VERIFY_URL}?secret={self.PRIVATE_KEY}&response={response}"
            )

            if self.CAPTCHA_LOG:
                self.debug_log(f"SEND REQUEST TO {self.GOOGLE_VERIFY_URL}")
                self.debug_log(
                    f"GOOGLE RESPONSE :\n{json.dumps(responseGoogle.json(), indent=4)}"
                )

            if responseGoogle.status_code == 200:
                jsonResponse = responseGoogle.json()
                return (
                    True
                    if jsonResponse["success"] and jsonResponse["score"] >= self.SCORE
                    else False
                )
            else:
                return False

    def renderWidget(self, *args, **kwargs) -> Markup:
        """render captcha widget

        :param id: id of captcha widget
        :type id: str

        :param css_class: css class of captcha widget
        :type css_class: str

        :param inline_css: inline css of captcha widget
        :type inline_css: str

        :param dataset: dataset of captcha widget
        :type dataset: str

        :param js_event: javascript event of captcha widget
        :type js_event: str

        :param button_text: value of input submit button of the form
        :type button_text: str

        :param parent_form_id: id of parent form element
        :type parent_form_id: str

        :param hide_badge: set visibility of captcha widget in bottom right corner,
            this parameter doesn't disable captcha, its only hidden the captcha in
            the page, but captcha still works
        :type hide_badge: bool

        :return: captcha widget
        :rtype: Markup
        """

        arg = ""
        arg += f"id=\"{kwargs.get('id')}\" \t" if kwargs.get("id") else ""
        arg += kwargs.get("dataset") + "\t" if kwargs.get("dataset") else ""
        arg += (
            f"style=\"{kwargs.get('inline_css')}\"\t"
            if kwargs.get("inline_css")
            else ""
        )
        arg += f"value=\"{kwargs.get('button_text', 'Submit')}\"\t"
        arg += f"{kwargs.get('js_event', ' ')}"

        captchaField = (
            f"""
            { self.HIDE_CAPTCHA_WIDGET_CSS if kwargs.get("hide_badge", "") == True else ''}
            <script src='https://www.google.com/recaptcha/api.js'></script>
            <script>function onSubmit(token) {{document.getElementById('{kwargs.get('parent_form_id', '')}').submit();}}</script>
            <input type='submit' class="g-recaptcha {kwargs.get('css_class', '')}" {arg}
             data-sitekey="{self.PUBLIC_KEY}" data-action="submit" data-callback="onSubmit"> </input>
            """
        ).strip()
        if self.ENABLED:
            return Markup(captchaField)
        else:
            # if captcha is disabled render just a simple submit input
            captchaField = f"""<input type='submit' class="{kwargs.get('class', '')}" {arg}></input>""".strip()
            return Markup(captchaField)
