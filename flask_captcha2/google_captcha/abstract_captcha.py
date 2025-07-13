from abc import ABC, abstractmethod

from flask import Flask
from markupsafe import Markup


class GoogleCaptchaInterface(ABC):
    """
    All Google Captcha related classes must implement
    all methods in this abstract base class.
    """

    @abstractmethod
    def init_app(self):
        """Initialize the captcha with the application context."""

    @abstractmethod
    def set_config(self, conf: dict) -> None:
        """Set the configuration for the captcha."""

    @abstractmethod
    def is_verify(self) -> bool:
        """Verify the captcha response."""

    @abstractmethod
    def render_widget(self) -> Markup:
        """Render the captcha widget in the UI."""


class BaseGoogleCaptcha:
    def refresh_conf(self, app: Flask) -> None:
        """Refresh the captcha object setting using the flask-application configuration"""
        self.__init__(app)
