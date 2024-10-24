"""
example :
    flask local image captcha
"""

import os
from flask import Flask, render_template, request
from flask_captcha2 import FlaskCaptcha

app = Flask(__name__)

app.config.update(
    {
        "SECRET_KEY": os.urandom(24),
        "CAPTCHA_IMAGE_ENABLE": True,  # captcha status <True, False> True: Production , False: development
        "CAPTCHA_IMAGE_LOG": True,  # show captcha logs in terminal > stdout
        # captcha settings
        "CAPTCHA_IMAGE_INCLUDE_LETTERS": True,
        "CAPTCHA_IMAGE_INCLUDE_NUMERIC": True,
        "CAPTCHA_IMAGE_INCLUDE_PUNCTUATION": False,
        # length of captcha string
        "CAPTCHA_IMAGE_CAPTCHA_LENGTH": 5,
        "CAPTCHA_IMAGE_HEIGHT": 120,
        "CAPTCHA_IMAGE_WIDTH":340,
    }
)

MainCaptcha = FlaskCaptcha(app=app)  # app is required
captcha = MainCaptcha.get_session_image_captcha(
    name="imageCaptcha"
)  # created a local Image captcha object, name is required


@app.post("/")
def index_post():
    if captcha.is_verify(captcha_answer=request.form.get("captcha")):
        # we should captcha answer to is_verify method
        return "captcha is ok"
    else:
        return "invalid captcha"


@app.get("/")
def index_get():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
