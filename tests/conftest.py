import os

import pytest
from flask import Flask

from flask_captcha2 import FlaskCaptcha


@pytest.fixture()
def app():
    """Main Flask Application fixture"""
    app = Flask(__name__)
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def googlecaptcha2_simple(app):
    """flask-captcha2 Google Captcha v2 object"""
    app.config.from_mapping(
        {
            "captcha_private_key": os.environ.get("PRIVATE_KEY_V2", "sample key"),
            "captcha_public_key": os.environ.get("PUBLIC_KEY_V2", "sample key"),
            "captcha_enabled": True,
            "captcha_log": False,
            "captcha_language": "en",
            "captcha_theme": "light",
            "captcha_size": "normal",
            "captcha_tabindex": 0,
            "captcha_type": "image",
        }
    )
    captcha_manager = FlaskCaptcha(app=app)
    captcha2 = captcha_manager.generate_google_captcha_v2(namespace="flask-captcha-v2")
    yield captcha2


@pytest.fixture()
def googlecaptcha2_hidden(app):
    """flask-captcha2 Google Captcha v2 object"""
    app.config.from_mapping(
        {
            "captcha_private_key": os.environ.get("PRIVATE_KEY_V2", "sample key"),
            "captcha_public_key": os.environ.get("PUBLIC_KEY_V2", "sample key"),
            "captcha_enabled": True,
            "captcha_log": False,
            "captcha_language": "en",
            "captcha_theme": "light",
            "captcha_size": "invisible",
            "captcha_tabindex": 0,
            "captcha_type": "invisible",
        }
    )
    captcha_manager = FlaskCaptcha(app=app)
    captcha2 = captcha_manager.generate_google_captcha_v2(namespace="flask-captcha-v2")
    yield captcha2


@pytest.fixture()
def googlecaptcha3(app):
    """flask-captcha2 Google Captcha v3 object"""
    app.config.from_mapping(
        {
            "captcha_private_key": os.environ.get("PRIVATE_KEY_V3", "test"),
            "captcha_public_key": os.environ.get("PRIVATE_KEY_V3", "test"),
            "captcha_enabled": True,  # captcha enable status
            "captcha_score": 0.5,
            "captcha_log": False,
        }
    )
    MainCaptcha = FlaskCaptcha(app=app)
    captcha = MainCaptcha.get_google_captcha_v3("flask-captcha-v3")
    yield captcha


@pytest.fixture()
def client(app):
    """Simple client for testing flask application"""
    yield app.test_client()


@pytest.fixture()
def captcha3_template_conf():
    """captcha version3 render_captcha config"""
    conf = {
        "parent_form_id": "id-of-parent-form",
        "button_text": "submit form",
        "dataset": ' data-check="True" data-another="Checked" ',
        "inline_css": 'background-color:"red"',
        "id": "id-of-submit-form",
        "css_class": "class-of-submit-form",
    }
    yield conf


@pytest.fixture()
def captcha2_simple_template_conf():
    """captcha version3 render_captcha config"""
    conf = {
        "namespace": "simple",
        "inline_css": "margin: 10px;",
        "css_class": "custom_css_class",
        "id": "captcha-v2",
        "dataset": "data-ok='true'",
    }
    yield conf


@pytest.fixture()
def captcha2_hidden_template_conf():
    """captcha version3 render_captcha config"""
    conf = {
        "namespace": "hidden",
        "inline_css": "margin: 10px;",
        "css_class": "form-control my-2 bg-success text-white fs-4",
        "id": "captcha-v2",
        "dataset": "data-ok='true'",
        "parent_form_id": "hidden_parent",
        "button_text": "Submit",
    }
    yield conf
