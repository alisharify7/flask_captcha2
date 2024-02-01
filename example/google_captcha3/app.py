"""
example :
    captcha version 3
"""

try:
    from dotenv import load_dotenv
except ImportError:
    raise ValueError("dotenv library is not installed, install it with `pip install python-dotenv` ")

import os

from flask import Flask, render_template

from flask_captcha2 import FlaskCaptcha

app = Flask(__name__)

load_dotenv()

app.config.update({
    "RECAPTCHA_PRIVATE_KEY": os.environ.get("PRIVATE_KEY_V3", ""),
    "RECAPTCHA_PUBLIC_KEY": os.environ.get("PRIVATE_KEY_V3", ""),
    'RECAPTCHA_ENABLED': True,  # captcha enable status
    "RECAPTCHA_SCORE": 0.5,  #
    "RECAPTCHA_LOG": True

})

Master_captcha = FlaskCaptcha(app=app)  # app is required
captcha = Master_captcha.getGoogleCaptcha3(name='captcha3')


@app.post("/")
def index_post():
    if captcha.is_verify():
        return "captcha is ok"
    else:
        return "invalid captcha"


@app.get("/")
def index_get():
    return render_template("login.html")


if __name__ == "__main__":
    app.run()
