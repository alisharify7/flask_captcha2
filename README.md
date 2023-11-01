# flask_captcha2
a light and simple Flask extension for integrating google recaptcha with Flask Apps
<p>
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/alisharify7/flask_captcha2">
  <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/alisharify7/flask_captcha2">
  <img alt="GitHub repo Licence" src="https://img.shields.io/pypi/l/flask_captcha2">
  
  [![PyPI version](https://badge.fury.io/py/flask-captcha2.svg)](https://badge.fury.io/py/flask-captcha2)

  total downloads: 
  
  [![Downloads](https://static.pepy.tech/badge/flask-captcha2)](https://pepy.tech/project/flask-captcha2)
  
  month downloads:
  
  [![Downloads](https://static.pepy.tech/badge/flask-captcha2/month)](https://pepy.tech/project/flask-captcha2)
  
  
  week downloads:
  
  [![Downloads](https://static.pepy.tech/badge/flask-captcha2/week)](https://pepy.tech/project/flask-captcha2)
  
  
</p>

### 0.0 how to install:
  
    pip install -U flask_captcha2 


### 0.1 how to use:
```python
from flask import Flask
from flask_captcha2.GoogleCaptcha import FlaskCaptcha2, FlaskCaptcha3

# `FlaskCaptcha3` is for Google Captcha version 3
# `FlaskCaptcha2` is for Google Captcha version 2

app = Flask(__name__)

# Captcha version 2 Configuration (I'm not a robot)
version_2_conf = {
  "RECAPTCHA_PRIVATE_KEY" : "Put Your private<secret> key here",
  "RECAPTCHA_PUBLIC_KEY" : "Put your public<site> key here",
  "RECAPTCHA_TABINDEX": "Tab index for Captcha Widget",
  "RECAPTCHA_LANGUAGE" : "Captcha Language <default en>",
  "RECAPTCHA_SIZE" : "Captcha Widget Size default normal <compact،, normal, invisible>",
  "RECAPTCHA_TYPE": "Captcha type default image",
  "RECAPTCHA_THEME" : "Captcha theme default light <dark, light>",
  "RECAPTCHA_ENABLED" : "Captcha status default True <True, False>",
  "RECAPTCHA_LOG": "Show captcha requests in stdout <True, False>"
}


# Captcha version 3 Configuration (invisible captcha)
version_3_conf = {
  "RECAPTCHA_PRIVATE_KEY" : "Put Your private<secret> key here",
  "RECAPTCHA_PUBLIC_KEY" : "Put your public<site> key here",
  "RECAPTCHA_ENABLED" : "Captcha status default True <True, False>",
  "RECAPTCHA_LOG": "Show captcha requests in stdout <True, False>",
  "RECAPTCHA_SCORE" : "Score for captcha <Float, between 0.5 to 1>"
}


# add config to flask app
app.config.from_mapping(version_2_conf) 
app.config.from_mapping(version_3_conf)

# Create a captcha instance
captcha2 = FlaskCaptcha2(app=app)
captcha3 = FlaskCaptcha3(app=app)

# or 
captcha2 = FlaskCaptcha2()
captcha3 = FlaskCaptcha3()

captcha2.init_app(app=app)
captcha3.init_app(app=app)
```

### 0.2 how use in templates for rendering Captcha Widget:

### Use < captchaField > Filter to render captcha in html


### Version 2 Captcha rendering:
```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Captcha version 2</title>
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

### Version 3 Captcha rendering:
```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Captcha version 3</title>
</head>
<body>
    
    <form method="POST" id="ParentForm">
        <input type="text" name="username">
        <input type="submit" value="submit">
        {# With captchaField filter you can render captcha widget in your html code #}
        {{ 
            captchaField
            ( {
                 'btnText': "Submit", # required
                 'ParentFormID': 'ParentForm', # required
            } ) 
        }}

<!--        
            full arguments in captcha version 3
            captchaField(
            {
                'btnText': "submit btn text", # required
                'ParentFormID': 'put prent form id here', # required
                'id':'if you want to set id for btn set id in here', # optional
                'style': 'css style', # optional
                'dataset': optional for giving dataset attribute to submit btn
                'hidden-badge':True or False, this value can hide or show captcha badge
            })
-->
        
    </form>
</body>
</html>
```


### 0.3 How verify Captcha:
### Use is_verify method  
```python
captcha = FlaskCaptcha2(app)
captcha = FlaskCaptcha3(app)

@app.route("/", methods=["POST"])
def index():
    # with is_verify method verify the captcha 
    if captcha.is_verify():
        return "Captcha is ok."
    else:
        return "Try again!" 

```




## Version History:


  - version 2.0.0 Released: May 18, 2023
  - Changes:
  
            None
  
  - version 2.0.1 Released: June 9, 2023
  - Changes:
  
        Change FlaskCaptcha Class to FlaskCaptcha2
        Fix bug in rendering captcha widget when captcha-enable was False

    
  - version 3.0.0 Released: September 9, 2023
  - Changes:
  
        change Package structure
        Add Captcha version 3 and fix some bugs in captcha version 2


  - version 3.0.2 Released: October 27, 2023
  - Changes:
  
        fix install error for version 3.0.0 and 3.0.1

