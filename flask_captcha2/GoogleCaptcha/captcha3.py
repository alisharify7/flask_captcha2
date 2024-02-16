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


class BaseCaptcha3(CommonCaptchaUtils):
    """
       Base Config for Google Captcha v3 class
    """
    PUBLIC_KEY: str = ''
    PRIVATE_KEY: str = ''
    ENABLED: bool = False
    SCORE: float = 0.5
    MINIMUM_SCORE: float = 0.5  # default minimum score
    CAPTCHA_LOG: bool = True
    GOOGLE_VERIFY_URL: str = "https://www.google.com/recaptcha/api/siteverify"

    Logger = get_logger(LogLevel=logging.DEBUG, CaptchaName="Google-Captcha-v3")



class FlaskCaptcha3(BaseCaptcha3):
    """
    Google Captcha version 3
        Score Base


    Env variables:
        CAPTCHA_PUBLIC_KEY <str:: public Key from googleDevelopers panel>
        CAPTCHA_PRIVATE_KEY <str:: public Key from googleDevelopers panel>
        CAPTCHA_SCORE <Float:: score for verify each request between 0.5 - 1>
        CAPTCHA_ENABLED <Boolean::captcha status>
        CAPTCHA_LOG <Boolean:: Show each Request Log in terminal>


    """

    def __init__(self, app: Flask = None, private_key: str = None, public_key: str = None, **kwargs):
        if app and isinstance(app, Flask):  # Flask app
            self.init_app(app)

        elif private_key and public_key:
            self.PUBLIC_KEY = public_key
            self.PRIVATE_KEY = private_key
            self.ENABLED = kwargs.get("enabled", self.ENABLED)
            self.CAPTCHA_LOG = kwargs.get("captcha_log", self.CAPTCHA_LOG)
            try:
                self.SCORE = self.MINIMUM_SCORE if int(kwargs.get('score', self.SCORE)) < self.MINIMUM_SCORE else int(kwargs.get('score', self.SCORE))
            except ValueError:
                self.SCORE = self.MINIMUM_SCORE

    def init_app(self, app: Flask = None):
        if not isinstance(app, Flask):
            raise ex.NotFlaskApp(f"{app} object is not a flask instance!")

        if not app.config.get("CAPTCHA_PUBLIC_KEY", None) or not app.config.get("CAPTCHA_PRIVATE_KEY", None):
            raise ValueError("Flask-Captcha2.GoogleCaptcha.captcha3: Private and Public Keys are Required")

        self.__init__(
            public_key=app.config.get("CAPTCHA_PUBLIC_KEY", None),
            private_key=app.config.get("CAPTCHA_PRIVATE_KEY", None),
            enabled=app.config.get("CAPTCHA_ENABLED", self.ENABLED),
            score=app.config.get("CAPTCHA_SCORE", self.SCORE),
            captcha_log=app.config.get("CAPTCHA_LOG", self.CAPTCHA_LOG)
        )

    def is_verify(self) -> bool:
        """ This Method Verify a Captcha v3 request
        
        Args: 
            None
        
        Returns:
            Bool: `True` if the captcha verified successfully from google otherwise `False`
        """
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
                self.debug_log(f"SEND REQUEST TO {self.GOOGLE_VERIFY_URL}")
                self.debug_log(f"GOOGLE RESPONSE :\n{json.dumps(responseGoogle.json(), indent=4)}")

            if responseGoogle.status_code == 200:
                jsonResponse = responseGoogle.json()
                return True if jsonResponse["success"] and jsonResponse["score"] >= self.SCORE else False
            else:
                return False

    def renderWidget(self, *args, **kwargs) -> Markup:
        """
            render captcha v3 widget

        Args:
            id: str: id of captcha element
            css: str: css of captcha element
            style: str: style of captcha element
            dataset: str: dataset of captcha element
            event: str: javascript event of captcha element
            BtnText: str: value of input submit button of the form
            ParentFormID: str: id of parent for element
            hiddenBadge: bool: set visibility of captcha widget in bottom right corner 


        Returns:
            captchaFiled: str<Markup>: captcha 
        """

        arg = ""
        arg += f"id=\"{kwargs.get('id')}\" \t" if kwargs.get('id') else ''  # id, class internal text
        arg += kwargs.get('dataset') + "\t" if kwargs.get('dataset') else ''  # dataset
        arg += f"style=\"{kwargs.get('style')}\"\t" if kwargs.get('style') else ''  # style
        arg += f"value=\"{kwargs.get('BtnText', 'Submit')}\"\t"  # style
        args += f"{kwargs.get('event', '')}"  # js event


        captchaField = (f"""
            {'<style>.grecaptcha-badge {visibility: hidden;}</style>' if kwargs.get("hiddenBadge", "") == True else ''}
            <script src='https://www.google.com/recaptcha/api.js'></script>
            <script>function onSubmit(token) {{document.getElementById('{kwargs.get('ParentFormID', '')}').submit();}}</script>
            <input type='submit' class="g-recaptcha {kwargs.get('class', '')}" {arg}
             data-sitekey="{self.PUBLIC_KEY}" data-action="submit" data-callback="onSubmit"> </input>
            """).strip()
        if self.ENABLED:
            return Markup(captchaField)
        else:
            # if captcha is disabled render just a simple submit input
            captchaField = f"""<input type='submit' class="{kwargs.get('class', '')}" {arg}></input>""".strip()
            return Markup(captchaField)
