class BaseFlaskCaptchaException(Exception):
    """Base FlaskCaptcha Exception """
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
