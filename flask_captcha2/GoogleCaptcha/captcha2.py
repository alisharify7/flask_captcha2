import json
import requests
from flask import request, Flask
from markupsafe import Markup
from flask_captcha2.Logger import get_logger



logger = get_logger()

class BaseCaptcha2:
    """
       Base Google Captcha v2 class
    """
    PUBLIC_KEY = None
    PRIVATE_KEY = None
    ENABLED = False
    CAPTCHA_LOG = True
    THEME = "light"
    TABINDEX = 0
    LANGUAGE = "en"
    TYPE = "image"
    SIZE = "normal" # compact، normal، invisible
    
    GOOGLE_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


class FlaskCaptcha2(BaseCaptcha2):
    """ Google Captcha version 2 """
    def __init__(self, app=None, public_key=None, private_key=None, **kwargs):
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


    def init_app(self, app=None):
        if not app.config.get("RECAPTCHA_PUBLIC_KEY", None) or not app.config.get("RECAPTCHA_PRIVATE_KEY", None):
            raise ValueError("Private and Public Keys are Required")

        self.__init__(
            public_key=app.config.get("RECAPTCHA_PUBLIC_KEY", None),
            private_key=app.config.get("RECAPTCHA_PRIVATE_KEY", None),
            enabled=app.config.get("RECAPTCHA_ENABLED", self.ENABLED),
            theme=app.config.get("RECAPTCHA_THEME", self.THEME),
            type=app.config.get("RECAPTCHA_TYPE", self.TYPE),
            size=app.config.get("RECAPTCHA_SIZE", self.SIZE),
            language=app.config.get("RECAPTCHA_LANGUAGE", self.LANGUAGE),
            tabindex=app.config.get("RECAPTCHA_TABINDEX", self.TABINDEX),
            captcha_log=app.config.get("RECAPTCHA_LOG", self.CAPTCHA_LOG)

        )

        @app.context_processor
        def render_captcha():
            return{"captchaField": self.renderWidget()}


    def is_verify(self):
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
                logger.info(f"RESPONSE RESPONSE GOOGLE CAPTCHA:\n {json.dumps(responseGoogle.json(), indent=4)}")


            if responseGoogle.status_code == 200:
                return responseGoogle.json()["success"]
            else:
                return False

    def renderWidget(self):
        """
            render captcha v2 widget
        :return:
        """
        CaptchaField = (f"""
        <script src='https://www.google.com/recaptcha/api.js'></script>
            <div class="g-recaptcha" data-sitekey="{self.PUBLIC_KEY}"
                data-theme="{self.THEME}" data-lang="{self.LANGUAGE}" data-type="{self.TYPE}" data-size="{self.SIZE}"
                data-tabindex="{self.TABINDEX}">
            </div>
        """) 
        if self.ENABLED:
            return Markup(CaptchaField)
        else: 
            return Markup(" ")
