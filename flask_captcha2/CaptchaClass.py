import flask
from flask import request
import requests
from markupsafe import Markup



class BaseCaptcha3:
    """
       Base Google Captcha v3 class
    """
    PUBLIC_KEY = None
    PRIVATE_KEY = None
    ENABLED = False
    THEME = "light"
    TABINDEX = 0
    LANGUAGE = "en"
    TYPE = "image"
    SIZE = "normal" # compact، normal، invisible
    SCORE = 0.5
    MINIMUM_SCORE = 0.5 # uses for captcha v3
    CAPTCHA_VISIBLE = False # uses for showing captcha v3
    
    GOOGLE_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


    
class FlaskCaptcha3(BaseCaptcha3):
    """ Google Captcha version 3 """

    def __init__(self, app=None, private_key=None, public_key=None, **kwargs):
        if app and isinstance(app, flask.Flask):
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
            self.SCORE = kwargs.get('score', self.SCORE)
            self.CAPTCHA_VISIBLE = kwargs.get('captcha_visible', self.CAPTCHA_VISIBLE)


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
            score=app.config.get("RECAPTCHA_SCORE", self.SCORE),
            captcha_visible=app.config.get("RECAPTCHA_VISIBLE", self.CAPTCHA_VISIBLE)
        )

        @app.context_processor
        def render_captcha():
            return{"captchaField": self.renderWidget}


    def is_verify(self):
        """ Verify a Captcha v3 """
        if not self.ENABLED:
            return True
        else:
            response = request.form.get('g-recaptcha-response', None)

            responseGoogle = requests.post(f"{self.GOOGLE_VERIFY_URL}?secret={self.PRIVATE_KEY}&response={response}")
            print(responseGoogle)
            print(responseGoogle.json())
            print(responseGoogle.text)

            # response from Google is something like this

            # {
            #      'success': True,
            #      'challenge_ts': '2023-04-04T07:39:45Z',
            #      'hostname': '127.0.0.1',
            #      'score': 0.9,
            #      'action': 'submit'
            # }

            #
            if responseGoogle.status_code == 200:
                jsonResponse = responseGoogle.json()
                return True if jsonResponse["success"] and jsonResponse["score"] >= self.SCORE else False
            else:
                return False

    def renderWidget(self, kw:dict={}) -> Markup:
        """
            render captcha v3 widget
        :return:
        """
        # {{
        #     captchaField(
        #     {
        #     'btnText': "submit btn text",
        #     'style': 'css style',
        #     'ParentFormID': 'put prent form id here',
        #     'id':'if you wanna set id for btn set id here',
        #     ''})
        # }}

        return Markup(f"""
        {'<style>.grecaptcha-badge {visibility: hidden;}</style>' if not self.CAPTCHA_VISIBLE else ''}
        <script src='//www.google.com/recaptcha/api.js'></script>
           <script>function onSubmit(token) {{document.getElementById('{kw.get('ParentFormID', '')}').submit();}}</script>
            <input type='submit' class="g-recaptcha {kw.get('class', '')}" 
            {kw.get('dataset', '')}
            id='{kw.get('id', '')}' value='{ kw.get('btnText', 'submit') }'
            style='{kw.get('style', '')}'
            data-sitekey="{self.PUBLIC_KEY}"
            data-action='submit'  
            data-callback='onSubmit'>
            </input>
        """) if self.ENABLED else Markup("")



class BaseCaptcha2:
    """
       Base Google Captcha v2 class
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

            #
            if responseGoogle.status_code == 200:
                return responseGoogle.json()["success"]
            else:
                return False

    def renderWidget(self):
        """
            render captcha v2 widget
        :return:
        """
        return Markup(f"""
        <script src='//www.google.com/recaptcha/api.js'></script>
            <div class="g-recaptcha" data-sitekey="{self.PUBLIC_KEY}"
                    data-theme="{self.THEME}" data-type="{self.TYPE}" data-size="{self.SIZE}"
                    data-tabindex="{self.TABINDEX}">
            </div>
        """) if self.ENABLED else ""
