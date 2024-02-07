"""
example :
    image captcha
"""

try:
    from dotenv import load_dotenv
except ImportError:
    raise ValueError("dotenv library is not installed, install it with `pip install python-dotenv` ")

import os

from flask import Flask, render_template, request
from flask_captcha2 import FlaskCaptcha

app = Flask(__name__)

load_dotenv()

app.config.update({
    "SECRET_KEY": os.urandom(24),
    'CAPTCHA_IMAGE_ENABLE': True,  # captcha enable status
    "CAPTCHA_IMAGE_LOG": True,
    "CAPTCHA_IMAGE_INCLUDE_LETTERS":True,
    "CAPTCHA_IMAGE_INCLUDE_NUMERIC": False,
    "CAPTCHA_IMAGE_INCLUDE_PUNCTUATION": False,
    "CAPTCHA_IMAGE_CAPTCHA_LENGTH": 4,
})


Master_captcha = FlaskCaptcha(app=app)  # app is required
captcha = Master_captcha.getLocalImageCaptcha(name='imageCaptcha')


@app.post("/")
def index_post():
    if captcha.is_verify(CaptchaAnswer=request.form.get("captcha")):
        return "captcha is ok"
    else:
        return "invalid captcha"


@app.get("/")
def index_get():
    return render_template("login.html")


if __name__ == "__main__":
    app.run()
