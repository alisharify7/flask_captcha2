"""
example :
    captcha version 2
"""

from flask import Flask, render_template
from flask_captcha2 import FlaskCaptcha2

app = Flask(__name__)

app.config.update({
    "RECAPTCHA_PRIVATE_KEY": '',
    "RECAPTCHA_PUBLIC_KEY":'',
    'RECAPTCHA_ENABLED':True, # captcha enable status
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