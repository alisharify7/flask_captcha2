import os

import pytest
from flask import Flask

from flask_captcha2 import FlaskCaptcha

"""By default captcha log is False"""


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
            "CAPTCHA_PRIVATE_KEY": os.environ.get("PRIVATE_KEY_V2", "sample key"),
            "CAPTCHA_PUBLIC_KEY": os.environ.get("PUBLIC_KEY_V2", "sample key"),
            'CAPTCHA_ENABLED': True,
            "CAPTCHA_LOG": False,
            "CAPTCHA_LANGUAGE": "en",
            "CAPTCHA_THEME": "light",
            "CAPTCHA_SIZE": "normal",
            "CAPTCHA_TABINDEX": 0,
            "CAPTCHA_TYPE": "image"
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
            "CAPTCHA_PRIVATE_KEY": os.environ.get("PRIVATE_KEY_V3", ""),
            "CAPTCHA_PUBLIC_KEY": os.environ.get("PRIVATE_KEY_V3", ""),
            'CAPTCHA_ENABLED': True,  # captcha enable status
            "CAPTCHA_SCORE": 0.5,  #
            "CAPTCHA_LOG": False,
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
    conf = {
        'parent_form_id': 'id-of-parent-form',
        'button_text': 'submit form',
        'dataset': ' data-check="True" data-another="Checked" ',
        'style': 'background-color:"red"',
        'id': 'id-of-submit-form',
        'class': 'class-of-submit-form',
        "CAPTCHA_LOG": False
    }
    yield conf
