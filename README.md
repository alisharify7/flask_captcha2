flask\_captcha2
===============

<img src="https://github.com/alisharify7/flask_captcha2/blob/main/docs/flask-captcha2.png?raw=true">

Flask plugin to integrate Google captcha (version 2, 3) and local
captcha (image, voice) with Flask applications

<a href="https://www.coffeete.ir/alisharify7">Donate/Support [Optional]</a>

<p>
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/alisharify7/flask_captcha2">
  <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/alisharify7/flask_captcha2">
  <img alt="GitHub repo Licence" src="https://img.shields.io/pypi/l/flask_captcha2">
  
[![Downloads](https://static.pepy.tech/badge/flask-captcha2)](https://pepy.tech/project/flask-captcha2)
[![Downloads](https://static.pepy.tech/badge/flask-captcha2/month)](https://pepy.tech/project/flask-captcha2)
  
  <br>
</p>

0.0 how to install:
-------------------

``` {.}
pip install -U flask_captcha2 
```

0.1 how to use:
---------------

```python
from flask import Flask
from flask_captcha2 import FlaskCaptcha

app = Flask(__name__)


 google_captcha2_config_list = {
     "CAPTCHA_PRIVATE_KEY": "hish !",
     "CAPTCHA_PUBLIC_KEY": "hish !",
     'CAPTCHA_ENABLED': True,  # captcha status <True, False> True: Production , False: development
     "CAPTCHA_LOG": True, # show captcha logs in console
     "CAPTCHA_LANGUAGE": "en" # captcha language
 }

 google_captcha3_config_list = {
     "CAPTCHA_PRIVATE_KEY": "hish !",
     "CAPTCHA_PUBLIC_KEY": "hish !",
     'CAPTCHA_ENABLED': True,  # captcha status <True, False> True: Production , False: development
     "CAPTCHA_SCORE": 0.5,  #google captcha version3 works with scores
     "CAPTCHA_LOG": True  # show captcha requests and logs in terminal > stdout
 }

 MasterCaptcha = FlaskCaptcha(app=app)  # app is required
 # passing config list directly
 google_captcha2 = MasterCaptcha.getGoogleCaptcha2(name='g-captcha2', conf=google_captcha2_config_list)
 google_captcha3 = MasterCaptcha.getGoogleCaptcha3(name='g-captcha3', conf=google_captcha3_config_list)
 # Names are important. Do not use repeated names and choose names with meaning
```

## example:
```python
# you can also pass nothing and it will be uses app.config for filling configs
 app.config.update(google_captcha3_config_list) # set configs in app.config
 Master_captcha = FlaskCaptcha(app=app)  # app is required
 # No need to send conf_list, it will be set automatically from app.config
 google_captcha2 = Master_captcha.getGoogleCaptcha2(name='g-captcha2')
```

0.2 how use in templates for rendering Captcha Widget:
------------------------------------------------------

#### Use < captcha.render_captcha > Filter to render a captcha in html

##### -> remember name argument in crating a captcha object

```python
google_captcha2 = Master_captcha.getGoogleCaptcha2(name='g-captcha2') # name
google_captcha3 = Master_captcha.getGoogleCaptcha3(name='g-captcha3') # name
```

for rendering a captcha width you should pass name to < model_name > in < captcha.render_captcha >

## rendering Google Version 2 Captcha:

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

 <form method="POST" action="some-url">
     <input placeholder="username" type="text" name="username" id="">
     <br>
     <input placeholder="password" type="password" name="password" id="">
     <br>
     <input value="submit" type="submit">

     {# model_name is required #}
     {{
         captcha.render_captcha (
                 model_name='g-captcha2', #{Required} name that are passed in getGoogleCaptcha2 method
                 class='custom-css-class-for-this-captcha', #[Optional] add class to captcha widget
                 style='text:red;', #[Optional] add inline style to captcha widget
                 id='g-captcha-v2', #[Optional] add id to captcha widget
                 dataset="data-checked='true';" #[Optional] add dataset to captcha widget
         )
     }}

 </form>

</body>
</html>
```

## rendering Google Version 3 Captcha :

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

 <form method="POST" action="/v3" id="ParentForm">
 {# you can also use Flask-wtf forms #}
 <input placeholder="username" type="text" name="username" id="">
 <br>
 <input placeholder="password" type="password" name="password" id="">
 <br>
 {{
     captcha.render_captcha (
             model_name='g-captcha3', #{Required} name that are passed in getGoogleCaptcha3 method
             class='custom-class-name', #[Optional] add css class to captcha widget
             id="SubmitBtnForm", #[Optional] add id to captcha widget
             style=" background-color:blue; color:white; font-size:2rem;", #[Optional] add style to captcha widget
             dataset="data-ok='true' data-test='test data set check' ", # [Optional]add dataset to captcha widget
             parent_form_id="ParentForm", #{Required} id of form that this captcha button is init
             button_text="submit This Form", #{Required} text context of submit button
             event=" onclick='alert('js alert');' ", #[Optional] add js event to captcha widget
             hide_badge=True #[Optional] hide captcha banner in page <its just hide it but captcha still works>
     )
 }}
 </form>
</body>
</html>
```

0.3 How to verify Captcha:
-----------------------

Use the is_verify method on captcha objects for validating a request that
contains a captcha 

```python
@app.route("/v2-verify/", methods=["POST"])
def index():
    # with is_verify method verify the captcha 
    if google_captcha2.is_verify():
        return "Captcha is ok."
    else:
        return "Try again!"

@app.route("/v3-verify/", methods=["POST"])
def index():
    # with the is_verify method verify the captcha
    if google_captcha3.is_verify():
        return "Captcha is ok."
    else:
        return "Try again!"
```

### Version History:

-   version 2.0.0 Released: May 18, 2023

-   Changes: - None

-   version 2.0.1 Released: June 9, 2023

-   Changes:

    > -   Change FlaskCaptcha Class to FlaskCaptcha2
    > -   Fix bug in rendering captcha widget when captcha-enable was False

-   version 3.0.0 Released: September 9, 2023

-   Changes:

    > -   Change package structure
    > -   Add Captcha version 3 and fix some bugs in Captcha version 2

-   version 3.0.4 Released: October 27, 2023
-   Changes:

    > -   reformat/Refactor project structure
    > -   adding FlaskCaptcha Master class
    > -   adding getFlaskCaptcha3 method for getting google-captcha
    >     version 3
    > -   adding getFlaskCaptcha2 method for getting google-captcha version 2
    > -   adding namespacing for each captcha
    > -   adding the ability to create multiple captchas with different versions
    > -   adding pytest base test

  
- version 3.0.5 Released: July 21, 2024
-   Changes:

    > -   reformat/Refactor code
    > -   rename render_captcha parameters
