"""
example :
    captcha version 2
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
    "CAPTCHA_PRIVATE_KEY": os.environ.get("PRIVATE_KEY_V2", ""),
    "CAPTCHA_PUBLIC_KEY": os.environ.get("PUBLIC_KEY_V2", ""),
    'CAPTCHA_ENABLED': True,  # captcha enable status
    "CAPTCHA_LOG": True,
    "CAPTCHA_LANGUAGE": "en"
})

Master_captcha = FlaskCaptcha(app=app)  # app is required
captcha = Master_captcha.getGoogleCaptcha2(name='captcha2')


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
