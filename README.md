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

# Flask-Captcha2
<img src="./docs/flask-captcha2.png">

### Flask plugin to integrate Google captcha (version 2, 3) and local captcha (image, voice) with Flask applications

### 0.0 how to install:
  
    pip install -U flask_captcha2 


### 0.1 how to use:
```python
from flask import Flask
from flask_captcha2 import FlaskCaptcha



app = Flask(__name__)

# Captcha version 2 Configuration (I'm not a robot)
google_captcha_version_2_conf = {
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
google_captcha_version_3_conf = {
  "RECAPTCHA_PRIVATE_KEY" : "Put Your private<secret> key here",
  "RECAPTCHA_PUBLIC_KEY" : "Put your public<site> key here",
  "RECAPTCHA_ENABLED" : "Captcha status default True <True, False>",
  "RECAPTCHA_LOG": "Show captcha requests in stdout <True, False>",
  "RECAPTCHA_SCORE" : "Score for captcha <Float, between 0.5 to 1>"
}


# create main captcha object
captcha = FlaskCaptcha(app=app)


# add config to flask app
app.config.from_mapping(google_captcha_version_2_conf)   
google_captcha_2 = captcha.getGoogleCaptcha2(name='first-google-captcha-v2') #-> return flask_captcha2.GoogleCaptcha.captcha2 object

app.config.from_mapping(google_captcha_version_3_conf)
google_captcha_3 = captcha.getGoogleCaptcha3(name='first-google-captcha-v3') #-> return flask_captcha2.GoogleCaptcha.captcha2 object


```

### 0.2 how use in templates for rendering Captcha Widget:

### Use < captcha.render_captcha > method to render captcha in html


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
        {# With captcha.render_captcha method you can render captcha widget in your html code #}
        {{ captcha.render_captcha(model_name='first-google-captcha-v2') }} 
        {# model_name should be exactly same as the name provided in getGoogleCaptcha2() method #}
        
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
        {# With captcha.render_captcha method you can render captcha widget in your html code #}
        {{ 
            captcha.render_captcha
            ( 
            model_name='first-google-captcha-v3',
            conf={
                     'ParentFormID': 'ParentForm', # required
                     'btnText': "Submit", # required
                } 
            ) 
        }}

<!--        
            full arguments in captcha version 3
            captcha.render_captcha(
            model_name='captcha object name',
            conf={
                'btn-text': "submit btn text", # required
                'parent-form-id': 'put prent form id here', # required
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

captcha = FlaskCaptcha(app=app)
google_captcha_2 = captcha.getGoogleCaptcha2(name='name-of-the-captcha')


@app.route("/", methods=["POST"])
def index():
    # with is_verify method verify the captcha in request
    if google_captcha_2.is_verify():
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

  - version 3.0.3 Released: -
  - Changes:
  
        change package structure
        adding object naming for each captcha object
            this feature helps us to create more than 1 captcha object in the app with 
            the previous version allowed us to only make 1 captcha object for the whole app.
            


