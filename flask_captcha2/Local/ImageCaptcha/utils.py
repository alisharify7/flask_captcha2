import os
import random
import base64

from captcha import image

from flask import Flask, session



class ImageCaptchaCONF:
    RECAPTCHA_KEY = ""
    RECAPTCHA_ENABLE = ""
    RECAPTCHA_LOG = ""
    RECAPTCHA_MIN = ""
    RECAPTCHA_MAX = ""
    RECAPTCHA_ALPHABET = ""
    RECAPTCHA_PUNCTUATION = ""


class ImageCaptcha(ImageCaptchaCONF):
    def __init__(self):
        pass

    def init_app(self):
        ...

    def __generate(self):
        pass

    def generate(self):
        pass

    def __validate(self):
        pass

    def validate(self):
        ...
