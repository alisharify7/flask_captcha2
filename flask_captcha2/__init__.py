from flask import request
import requests
from markupsafe import Markup


class Captcha:
    """
       Base Class For captcha object in app
    """
    PUBLIC_KEY = None
    PRIVATE_KEY = None
    ENABLED = False
    THEME = "light",
    TABINDEX = 0
    LANGUAGE = "en"
    TYPE = "image"
    SIZE = "normal" # compact، normal، invisible

    GOOGLE_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


class FlaskCaptcha(Captcha):

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
            tabindex=app.config.get("RECAPTCHA_TABINDEX", self.TABINDEX)
        )
        @app.context_processor
        def render_captcha():
            return{"captchaField": self.renderWidget()}


    def is_verify(self):
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

            #
            if responseGoogle.status_code == 200:
                return responseGoogle.json()["success"]
            else:
                return False

    def renderWidget(self):
        """
            render captcha widget
        :return:
        """
        return Markup(f"""
        <script src='//www.google.com/recaptcha/api.js'></script>
            <div class="g-recaptcha" data-sitekey="{self.PUBLIC_KEY}"
                    data-theme="{self.THEME}" data-type="{self.TYPE}" data-size="{self.SIZE}"
                    data-tabindex="{self.TABINDEX}">
            </div>
        """)