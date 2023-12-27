import json
from flask import request, Flask
import requests
from markupsafe import Markup
from flask_captcha2.Logger import get_logger

logger = get_logger()


class BaseCaptcha3:
    """
       Base Config for Google Captcha v3 class
    """
    PUBLIC_KEY: str = None
    PRIVATE_KEY: str = None
    ENABLED: bool = False
    SCORE: float = 0.5
    MINIMUM_SCORE: float = 0.5  # default minimum score
    CAPTCHA_LOG: bool = True
    GOOGLE_VERIFY_URL: str = "https://www.google.com/recaptcha/api/siteverify"


class FlaskCaptcha3(BaseCaptcha3):
    """ 
    Google Captcha version 3
        Scoere Base


    Env variables:
        RECAPTCHA_PUBLIC_KEY <str:: public Key from googleDevelopers panel>
        RECAPTCHA_PRIVATE_KEY <str:: public Key from googleDevelopers panel>
        RECAPTCHA_SCORE <Float:: score for verify each request between 0.5 - 1>
        RECAPTCHA_ENABLED <Boolean::captcha status>
        RECAPTCHA_LOG <Boolean:: Show each Request Log in terminal>

    
    """

    def __init__(self, app: Flask = None, private_key: str = None, public_key: str = None, **kwargs):
        if app and isinstance(app, Flask):  # Flask app
            self.init_app(app)

        elif private_key and public_key:
            self.PUBLIC_KEY = public_key
            self.PRIVATE_KEY = private_key
            self.ENABLED = kwargs.get("enabled", self.ENABLED)
            try:
                self.SCORE = self.MINIMUM_SCORE if int(kwargs.get('score', self.SCORE)) < self.MINIMUM_SCORE else int(
                    kwargs.get('score', self.SCORE))
            except ValueError:
                self.SCORE = self.MINIMUM_SCORE

            self.CAPTCHA_LOG = kwargs.get("captcha_log", self.CAPTCHA_LOG)

    def init_app(self, app: Flask = None):
        if not app.config.get("RECAPTCHA_PUBLIC_KEY", None) or not app.config.get("RECAPTCHA_PRIVATE_KEY", None):
            raise ValueError("Private and Public Keys are Required")

        self.__init__(
            public_key=app.config.get("RECAPTCHA_PUBLIC_KEY", None),
            private_key=app.config.get("RECAPTCHA_PRIVATE_KEY", None),
            enabled=app.config.get("RECAPTCHA_ENABLED", self.ENABLED),
            score=app.config.get("RECAPTCHA_SCORE", self.SCORE),
            captcha_log=app.config.get("RECAPTCHA_LOG", self.CAPTCHA_LOG)
        )

        @app.context_processor
        def render_captcha() -> dict:
            return {"captchaField": self.renderWidget}

    def is_verify(self) -> bool:
        """ Verify request that contain captcha v3 """
        if not self.ENABLED:
            return True
        else:
            response = request.form.get('g-recaptcha-response', None)

            responseGoogle = requests.post(f"{self.GOOGLE_VERIFY_URL}?secret={self.PRIVATE_KEY}&response={response}")

            # response from Google is something like this
            # {
            #      'success': True,
            #      'challenge_ts': '2023-04-04T07:39:45Z',
            #      'hostname': '127.0.0.1',
            #      'score': 0.9,
            #      'action': 'submit'
            # }

            if self.CAPTCHA_LOG:
                logger.info(f"SEND REQUEST TO {self.GOOGLE_VERIFY_URL}")
                logger.info(f"GOOGLE RESPONSE :\n{json.dumps(responseGoogle.json(), indent=4)}")

            if responseGoogle.status_code == 200:
                jsonResponse = responseGoogle.json()
                return True if jsonResponse["success"] and jsonResponse["score"] >= self.SCORE else False
            else:
                return False

    def renderWidget(self, kw: dict = {}) -> Markup:
        """
            render captcha v3 widget
        :return: 
        """
        # {{  
        #         how use context_processor in template
        #     captchaField
        #     ({
        #         'btnText': "submit btn text", # required
        #         'ParentFormID': 'put prent form id here', # required
        #         'id':'if you want to set id for btn set id in here', # optional
        #         'style': 'css style', # optional
        #         'dataset': optional for giving dataset attribute to submit btn
        #         'hidden-badge':True or False, this value can hide or show captcha badge
        #     })
        # }}
        captchaField = (f"""
            {'<style>.grecaptcha-badge {visibility: hidden;}</style>' if kw.get("hidden-badge", "") == True else ''}
            <script src='https://www.google.com/recaptcha/api.js'></script>
            <script>function onSubmit(token) {{document.getElementById('{kw.get('ParentFormID', '')}').submit();}}</script>
            <input type='submit' class="g-recaptcha {kw.get('class', '')}" 
            {kw.get('dataset', '')}
            {'id=' + kw.get('id', '') if kw.get('id', '') else ''}
            value='{kw.get('btnText', 'submit')}'
            {'style=' + "'" + kw.get('style', '') + "'" if kw.get('style', '') else ''}
            data-sitekey="{self.PUBLIC_KEY}"
            data-action='submit'  
            data-callback='onSubmit'>
            </input>
        """)
        if self.ENABLED:
            return Markup(captchaField)
        else:
            return Markup("")
