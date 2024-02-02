import os

import pytest
from flask import Flask

from flask_captcha2 import FlaskCaptcha


@pytest.fixture()
def app():
    """Main Flask Application fixture"""
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
        # 'DEBUG': True
    })

    yield app


@pytest.fixture()
def googlecaptcha2(app):
    """flask-captcha2 Google Captcha v2 object"""
    app.config.from_mapping(
        {
            "RECAPTCHA_PRIVATE_KEY": os.environ.get("PRIVATE_KEY_V2", "sample key"),
            "RECAPTCHA_PUBLIC_KEY": os.environ.get("PUBLIC_KEY_V2", "sample key"),
            'RECAPTCHA_ENABLED': True,
            "RECAPTCHA_LOG": True,
            "RECAPTCHA_LANGUAGE": "en",
            "RECAPTCHA_THEME": "light",
            "RECAPTCHA_SIZE": "normal",
            "RECAPTCHA_TABINDEX": 0,
            "RECAPTCHA_TYPE": "image"
        }
    )
    Master_captcha = FlaskCaptcha(app=app)
    captcha = Master_captcha.getGoogleCaptcha2('flask-captcha-v2')
    yield captcha


@pytest.fixture()
def googlecaptcha3(app):
    """flask-captcha2 Google Captcha v3 object"""
    app.config.from_mapping(
        {
            "RECAPTCHA_PRIVATE_KEY": os.environ.get("PRIVATE_KEY_V3", ""),
            "RECAPTCHA_PUBLIC_KEY": os.environ.get("PRIVATE_KEY_V3", ""),
            'RECAPTCHA_ENABLED': True,  # captcha enable status
            "RECAPTCHA_SCORE": 0.5,  #
            "RECAPTCHA_LOG": True,

        }
    )
    Master_captcha = FlaskCaptcha(app=app)
    captcha = Master_captcha.getGoogleCaptcha3('flask-captcha-v3')

    yield captcha


@pytest.fixture()
def client(app):
    """Simple client for testing flask application"""
    yield app.test_client()



@pytest.fixture()
def captcha3_template_conf():
    """captcha version3 render_captcha config"""
    conf ={
            'parent-form-id': 'id-of-parent-form',
            'btn-text': 'submit form',
            'dataset':' data-check="True" data-another="Checked" ',
            'style': 'background-color:"red"',
            'id': 'id-of-submit-form',
            'class': 'class-of-submit-form'
        }
    yield conf