flask_captcha2
==============

an light and simple flask extension for integrate google recaptcha with
Flask Apps

.. raw:: html

   <p>

|PyPI version|

.. raw:: html

   </p>

0.0 how to install:
~~~~~~~~~~~~~~~~~~~

::

   pip install -U flask_captcha2 

0.1 how to use:
~~~~~~~~~~~~~~~

.. code:: python

   from flask import Flask
   from flask_captcha2 import FlaskCaptcha2

   app = Flask(__name__)

   # update app config
   app.config["RECAPTCHA_PRIVATE_KEY"] = "Private key"
   app.config["RECAPTCHA_PUBLIC_KEY"] = "Public Key"
   app.config["RECAPTCHA_ENABLED"] = True or False

   # create captcha instance
   captcha = FlaskCaptcha2(app)

0.2 how use in template for rendering Captcha Widget:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use < captchaField > Filter to render captcha in html
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: html

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

0.3 How verify Captcha:
~~~~~~~~~~~~~~~~~~~~~~~

Use is_verify method
~~~~~~~~~~~~~~~~~~~~

.. code:: python

   captcha = FlaskCaptcha2(app)

   @app.route("/", methods=["POST"])
   def index():
       # with is_verify method verify the captcha 
       if captcha.is_verify():
           return "Captcha is ok."
       else:
           return "Try again!" 

Configuration :
^^^^^^^^^^^^^^^

::

   RECAPTCHA_PRIVATE_KEY = "Put Your private<secret> key here"
   RECAPTCHA_PUBLIC_KEY = "Put your public<site> key here"
   RECAPTCHA_TABINDEX= "Tab index for Captcha Widget"
   RECAPTCHA_LANGUAGE = "Captcha Language <default en>"
   RECAPTCHA_SIZE = "Captcha Widget Size default normal <compact،, normal, invisible>"
   RECAPTCHA_TYPE = "Captcha type default image"
   RECAPTCHA_THEME = "Captcha theme default light <dark, light>"
   RECAPTCHA_ENABLED = "Captcha status default True <True, False>"

Set configuration :
===================

.. code:: python

       from flask import Flask
       from flask_captcha2 import FlaskCaptcha2
       
       app = Flask(__name__)
       
       app.config["RECAPTCHA_PRIVATE_KEY"] = "Put Your private<secret> key here"
       app.config["RECAPTCHA_PUBLIC_KEY"] = "Put your public<site> key here"
       app.config["RECAPTCHA_TABINDEX"] = "Tab index for Captcha Widget"
       app.config["RECAPTCHA_LANGUAGE"] = "Captcha Language <default en>"
       app.config["RECAPTCHA_SIZE"] = "Captcha Widget Size default normal <compact،, normal, invisible>"
       app.config["RECAPTCHA_TYPE"] = "Captcha type default image"
       app.config["RECAPTCHA_THEME"] = "Captcha theme default light <dark, light>"
       app.config["RECAPTCHA_ENABLED"] = "Captcha status default True <True, False>"

       captcha = FlaskCaptcha2(app)
       or 
       captcha = FlaskCaptcha2()
       captcha.init_app(app)
       
       

Version History:
----------------

-  version 2.0.0 Released: May 18, 2023

-  Changes:

   ::

          None

-  version 2.0.1 Released: 0.0.0.

-  Changes:

   ::

      Change FlaskCaptcha Class to FlaskCaptcha2

.. |PyPI version| image:: https://badge.fury.io/py/flask-captcha2.svg
   :target: https://badge.fury.io/py/flask-captcha2
