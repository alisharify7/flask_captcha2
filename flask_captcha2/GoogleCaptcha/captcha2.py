import json

import requests
from flask import request, Flask
from markupsafe import Markup

from flask_captcha2 import excep as ex
from flask_captcha2.Logger import get_logger
from .utils import CommandCaptchaUtils

logger = get_logger("Google-Captcha-v2")


class BaseCaptcha2(CommandCaptchaUtils):
    """
       Base Google Captcha v2 class
    """
    PUBLIC_KEY: str = None
    PRIVATE_KEY: str = None
    CAPTCHA_LOG: bool = True
    ENABLED: bool = False
    THEME: str = "light"
    TABINDEX: int = 0
    LANGUAGE: str = "en"
    TYPE: str = "image"
    SIZE: str = "normal"  # compact، normal، invisible
    GOOGLE_VERIFY_URL: str = "https://www.google.com/recaptcha/api/siteverify"


class FlaskCaptcha2(BaseCaptcha2):
    """ Google Captcha version 2 """

    def __init__(self, app: Flask = None, public_key: str = None, private_key: str = None, **kwargs):
        if app:
            self.init_app(app)

        elif private_key and public_key:
            self.PUBLIC_KEY = public_key
            self.PRIVATE_KEY = private_key
            self.ENABLED = kwargs.get("enabled", self.ENABLED)
            self.THEME = kwargs.get('theme', self.THEME)
            self.TYPE = kwargs.get('type', self.TYPE)
            self.SIZE = kwargs.get('size', self.SIZE)
            self.TABINDEX = kwargs.get('tabindex', self.TABINDEX)
            self.LANGUAGE = kwargs.get('language', self.LANGUAGE)
            self.CAPTCHA_LOG = kwargs.get('captcha_log', self.CAPTCHA_LOG)

    def init_app(self, app: Flask = None):
        if not isinstance(app, Flask):
            raise ex.NotFlaskApp(f"{app} object is not a flask instance!")

        if not app.config.get("CAPTCHA_PUBLIC_KEY", None) or not app.config.get("CAPTCHA_PRIVATE_KEY", None):
            raise ValueError("Flask-Captcha2.GoogleCaptcha.captcha2: Private and Public Keys are Required")

        self.__init__(
            public_key=app.config.get("CAPTCHA_PUBLIC_KEY", None),
            private_key=app.config.get("CAPTCHA_PRIVATE_KEY", None),
            enabled=app.config.get("CAPTCHA_ENABLED", self.ENABLED),
            theme=app.config.get("CAPTCHA_THEME", self.THEME),
            type=app.config.get("CAPTCHA_TYPE", self.TYPE),
            size=app.config.get("CAPTCHA_SIZE", self.SIZE),
            language=app.config.get("CAPTCHA_LANGUAGE", self.LANGUAGE),
            tabindex=app.config.get("CAPTCHA_TABINDEX", self.TABINDEX),
            captcha_log=app.config.get("CAPTCHA_LOG", self.CAPTCHA_LOG)

        )

    def is_verify(self) -> bool:
        """ Verify a Captcha v2 """
        if not self.ENABLED:
            return True
        else:
            data = {
                "secret": self.PRIVATE_KEY,
                "response": request.form.get('g-recaptcha-response', None),
            }

            responseGoogle = requests.get(self.GOOGLE_VERIFY_URL, params=data)
            # response from Google is something like this
            # {
            #     "success": true,
            #     "challenge_ts": "2023-05-17T10:41:22Z",
            #     "hostname": "127.0.0.1"
            # }
            # {
            #     "success": false,
            #     "error-codes": [
            #         "invalid-input-response"
            #     ]
            # }
            if self.CAPTCHA_LOG:
                logger.info(f"SEND REQUEST TO {self.GOOGLE_VERIFY_URL}")
                logger.info(f"GOOGLE RESPONSE:\n {json.dumps(responseGoogle.json(), indent=4)}")

            if responseGoogle.status_code == 200:
                return responseGoogle.json()["success"]
            else:
                return False

    def renderWidget(self, *args, **kwargs) -> Markup:
        """
            render captcha v2 widget
        :return:
        """

        args = ""
        args += f"id=\"{kwargs.get('id')}\"\t" if kwargs.get('id') else ''  # id, class internal text
        args += kwargs.get('dataset') + "\t" if kwargs.get('dataset') else ''  # dataset
        args += f"style=\"{kwargs.get('style')}\"\t" if kwargs.get('style') else ''  # style

        CaptchaField = (f"""
        <script src='https://www.google.com/recaptcha/api.js'></script>
            <div class="g-recaptcha {kwargs.get('class', '')}" data-sitekey="{self.PUBLIC_KEY}"
                data-theme="{self.THEME}" data-lang="{self.LANGUAGE}" data-type="{self.TYPE}" data-size="{self.SIZE}"
                data-tabindex="{self.TABINDEX}" {args}>
            </div>
        """).strip()
        if self.ENABLED:
            return Markup(CaptchaField)
        else:
            return Markup(" ")
