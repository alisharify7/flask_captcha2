from abc import ABC, abstractmethod

class GoogleCaptchaInterface(ABC):
    """
    All Google Captcha related classes must implement 
    all methods in this abstract base class.
    """

    @abstractmethod
    def set_config(self):
        """Set the configuration for the captcha."""
        pass

    @abstractmethod
    def is_verify(self):
        """Verify the captcha response."""
        pass

    @abstractmethod
    def render_widget(self):
        """Render the captcha widget in the UI."""
        pass

    @abstractmethod
    def init_app(self):
        """Initialize the captcha with the application context."""
        pass
