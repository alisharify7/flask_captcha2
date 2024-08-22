"""
 * flask_captcha2 OSS
 * author: github.com/alisharify7
 * email: alisharifyofficial@gmail.com
 * license: see LICENSE for more details.
 * Copyright (c) 2023 - ali sharifi
 * https://github.com/alisharify7/flask_captcha2
"""

class BaseFlaskCaptchaException(Exception):
    """Base FlaskCaptcha Exception"""

    ...


class NotFlaskApp(BaseFlaskCaptchaException):
    """Custom exception class
    this exception raise when an invalid or wrong
    app passed in __init__ or init_app function
    """

    ...


class CaptchaNameNotExists(BaseFlaskCaptchaException):
    """Custom exception class
    this exception raise when render_captcha func get wrong model name
    """

    ...
