"""
example :
    google captcha version 3
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
        "CAPTCHA_PRIVATE_KEY": os.environ.get("PRIVATE_KEY_V3", ""),
        "CAPTCHA_PUBLIC_KEY": os.environ.get("PUBLIC_KEY_V3", ""),
        "CAPTCHA_ENABLED": True,  # captcha status <True, False> True: Production , False: development
        "CAPTCHA_SCORE": 0.5,  # google captcha version3 works with scores
        "CAPTCHA_LOG": True,  # show captcha requests and logs in terminal > stdout
    }
)

Master_captcha = FlaskCaptcha(app=app)  # app is required
captcha = Master_captcha.get_google_captcha_v3(
    name="captcha3"
)  # created a google captcha object


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
    app.run(debug=True)
