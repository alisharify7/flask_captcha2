"""
example :
    image captcha
"""

import os

from flask import Flask, render_template, request

from flask_captcha2 import FlaskCaptcha

app = Flask(__name__)

app.config.update({
    "SECRET_KEY": os.urandom(24),
    'CAPTCHA_IMAGE_ENABLE': True,  # captcha enable status
    "CAPTCHA_IMAGE_LOG": True,
    "CAPTCHA_IMAGE_INCLUDE_LETTERS": True,
    "CAPTCHA_IMAGE_INCLUDE_NUMERIC": True,
    "CAPTCHA_IMAGE_INCLUDE_PUNCTUATION": False,
    "CAPTCHA_IMAGE_CAPTCHA_LENGTH": 4,
})

MainCaptcha = FlaskCaptcha(app=app)  # app is required
captcha = MainCaptcha.getLocalImageCaptcha(name='imageCaptcha')
captcha.Logger.info("KJO")


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
    app.run(debug=True)
