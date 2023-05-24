# flask_captcha2
an light and simple flask extension for integrate google recaptcha with Flask Apps
<p>

  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/alisharify7/flask_captcha2">

  <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/alisharify7/flask_captcha2">
  
  [![PyPI version](https://badge.fury.io/py/flask-captcha2.svg)](https://badge.fury.io/py/flask-captcha2)

</p>
  
.. image:: https://img.shields.io/pypi/l/flask_captcha2
  :target: https://github.com/mbi/flask_captcha2/blob/master/LICENSE



### 0.0 how to install:
  
    pip install -U flask_captcha2 


### 0.1 how to use:

```python
from flask import Flask
from flask_captcha2 import FlaskCaptcha

app = Flask(__name__)

# update app config
app.config["RECAPTCHA_PRIVATE_KEY"] = "Private key"
app.config["RECAPTCHA_PUBLIC_KEY"] = "Public Key"
app.config["RECAPTCHA_ENABLED"] = True or False

# create captcha instance
captcha = FlaskCaptcha(app)

```

### 0.2 how use in template for rendering Captcha Widget:

### Use < captchaField > Filter to render captcha in html


```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
    <form method="POST">
        <input type="text" name="username">
        <input type="submit" value="submit">
        {# With captchaField filter you can render captcha widget in your html code #}
        {{ captchaField }}
    </form>
</body>
</html>
```


### 0.3 How verify Captcha:
### Use is_verify method  
```python
captcha = FlaskCaptcha(app)

@app.route("/", methods=["POST"])
def index():
    # with is_verify method verify the captcha 
    if captcha.is_verify():
        return "Captcha is ok."
    else:
        return "Try again!" 

```


#### Configuration :
  
    RECAPTCHA_PRIVATE_KEY = "Put Your private<secret> key here"
    RECAPTCHA_PUBLIC_KEY = "Put your public<site> key here"
    RECAPTCHA_TABINDEX= "Tab index for Captcha Widget"
    RECAPTCHA_LANGUAGE = "Captcha Language <default en>"
    RECAPTCHA_SIZE = "Captcha Widget Size default normal <compact،, normal, invisible>"
    RECAPTCHA_TYPE = "Captcha type default image"
    RECAPTCHA_THEME = "Captcha theme default light <dark, light>"
    RECAPTCHA_ENABLED = "Captcha status default True <True, False>"
