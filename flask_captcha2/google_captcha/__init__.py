"""
* flask_captcha2 OSS
* main import entrypoint
* author: github.com/alisharify7
* email: alisharifyofficial@gmail.com
* license: see LICENSE for more details.
* Copyright (c) 2023 - ali sharifi
* https://github.com/alisharify7/flask_captcha2
"""

from .captcha2 import GoogleCaptcha2
from .captcha3 import GoogleCaptcha3

__all__ = (
    "GoogleCaptcha2",
    "GoogleCaptcha3",
)
