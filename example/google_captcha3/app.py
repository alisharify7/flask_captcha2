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

app.config.update()
captcha_manager = FlaskCaptcha(app=app)  # app is required
google_captcha_v3 = captcha_manager.generate_google_captcha_v3(
    namespace="captcha3",
    conf={
        "captcha_private_key": os.environ.get("captcha_private_key", ""),
        "captcha_public_key": os.environ.get("captcha_public_key", ""),
        "captcha_enabled": True,  # captcha status <True, False> True: Production , False: development
        "captcha_score": 0.5,  # google captcha version3 works with scores
        "captcha_log": True,  # show captcha requests and logs in terminal > stdout
    },
)  # generate google captcha v3 object

another_google_captcha_v3 = captcha_manager.generate_google_captcha_v3(
    namespace="another_captcha3",
    conf={
        "captcha_private_key": os.environ.get("captcha_private_key", ""),
        "captcha_public_key": os.environ.get("captcha_public_key", ""),
        "captcha_enabled": True,  # captcha status <True, False> True: Production , False: development
        "captcha_score": 0.5,  # google captcha version3 works with scores
        "captcha_log": True,  # show captcha requests and logs in terminal > stdout
    },
)  # generate google captcha v3 object


@app.post("/")
def index_post():
    if google_captcha_v3.is_verify():
        return "captcha is ok"
    else:
        return "invalid captcha"


@app.get("/")
def index_get():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
