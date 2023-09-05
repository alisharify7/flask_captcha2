"""
example :
    captcha version 3
"""

from flask import Flask, render_template
from flask_captcha2 import FlaskCaptcha3

app = Flask(__name__)

app.config.update({
    "RECAPTCHA_PRIVATE_KEY": 'secret key',
    "RECAPTCHA_PUBLIC_KEY":'public key',
    'RECAPTCHA_ENABLED':True, # captcha enable status
    "RECAPTCHA_SCORE": 0.5, # 
    "RECAPTCHA_LOG": True

})

captcha = FlaskCaptcha3()
captcha.init_app(app=app)
# or 
# captcha = FlaskCaptcha3(app=app)


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