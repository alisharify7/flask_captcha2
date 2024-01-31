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
from flask_captcha2 import FlaskCaptcha2


app = Flask(__name__)

load_dotenv()

app.config.update({
    "RECAPTCHA_PRIVATE_KEY": os.environ.get("PRIVATE_KEY_V2", ""),
    "RECAPTCHA_PUBLIC_KEY": os.environ.get("PUBLIC_KEY_V2", ""),
    'RECAPTCHA_ENABLED': True,  # captcha enable status
    "RECAPTCHA_LOG": True,
    "RECAPTCHA_LANGUAGE": "en"
})

captcha = FlaskCaptcha2()
captcha.init_app(app=app)
# or
# captcha = FlaskCaptcha2(app=app)


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
