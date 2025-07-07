"""
example :
    google captcha version 2
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

load_dotenv()

app.config.update(
    {
        "captcha_private_key": os.environ.get("captcha_private_key", ""),
        "captcha_public_key": os.environ.get("captcha_public_key", ""),
        "captcha_enabled": True,  # captcha status <True, False> True: Production , False: development
        "captcha_log": True,  # show captcha logs in console
        "captcha_language": "en",  # captcha language
    }
)

captcha_manager = FlaskCaptcha(app=app)  # app is required
google_captcha_version3 = captcha_manager.generate_google_captcha_v2(
    namespace="captcha2"
)  # created a Google captcha v2 object


@app.post("/")
def index_post():
    """index view: post method"""
    if google_captcha_version3.is_verify():
        return "captcha is ok"
    else:
        return "invalid captcha"


@app.get("/")
def index_get():
    """index view: get method"""
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555, threaded=False)
