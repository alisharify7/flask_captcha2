"""
example :
    google captcha version 2 and version 3 together
"""

try:
    from dotenv import load_dotenv
except ImportError:
    raise ValueError(
        "dotenv library is not installed, install it with `pip install python-dotenv` "
    )

import os
from flask import Flask, render_template
from flask_captcha2 import FlaskCaptcha

app = Flask(__name__)

load_dotenv()  # load all environment variables

# creating each captcha object config
google_captcha2_config_list = {
    "CAPTCHA_PRIVATE_KEY": os.environ.get("PRIVATE_KEY_V2", ""),
    "CAPTCHA_PUBLIC_KEY": os.environ.get("PUBLIC_KEY_V2", ""),
    "CAPTCHA_ENABLED": True,  # captcha status <True, False> True: Production , False: development
    "CAPTCHA_LOG": True,  # show captcha logs in console
    "CAPTCHA_LANGUAGE": "en",  # captcha language
}

google_captcha3_config_list = {
    "CAPTCHA_PRIVATE_KEY": os.environ.get("PRIVATE_KEY_V3", ""),
    "CAPTCHA_PUBLIC_KEY": os.environ.get("PUBLIC_KEY_V3", ""),
    "CAPTCHA_ENABLED": True,  # captcha status <True, False> True: Production , False: development
    "CAPTCHA_SCORE": 0.5,  # google captcha version3 works with scores
    "CAPTCHA_LOG": True,  # show captcha requests and logs in terminal > stdout
}

Master_captcha = FlaskCaptcha(app=app)  # app is required
google_captcha2 = Master_captcha.get_google_captcha_v2(
    name="g-captcha2", conf=google_captcha2_config_list
)  # pass config directly to method
google_captcha3 = Master_captcha.get_google_captcha_v3(
    name="g-captcha3", conf=google_captcha3_config_list
)  # pass config directly to method


@app.post("/v3")
def submit_captcha_version3_post():
    """validate a google-captcha version3"""
    if google_captcha3.is_verify():
        return "google captcha version3 is ok"
    else:
        return "invalid captcha"


@app.post("/v2")
def submit_captcha_version2_post():
    """validate a google-captcha version2"""
    if google_captcha2.is_verify():
        return "google captcha version2 is ok"
    else:
        return "invalid captcha"


@app.get("/")
def index_get():
    """index view: get method"""
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
