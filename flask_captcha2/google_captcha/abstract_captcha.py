from abc import ABC, abstractmethod
from markupsafe import Markup


class GoogleCaptchaInterface(ABC):
    """
    All Google Captcha related classes must implement 
    all methods in this abstract base class.
    """
    @abstractmethod
    def init_app(self):
        """Initialize the captcha with the application context."""
        pass

    @abstractmethod
    def set_config(self, conf: dict) -> None:
        """Set the configuration for the captcha."""
        pass

    @abstractmethod
    def is_verify(self) -> bool:
        """Verify the captcha response."""
        pass

    @abstractmethod
    def render_widget(self) -> Markup:
        """Render the captcha widget in the UI."""
        pass

