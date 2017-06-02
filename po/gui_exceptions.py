from selenium.common.exceptions import WebDriverException

class UIError(Exception):
    """ Base class for exceptions related to error in the tested UI."""
    def __init__(self, *args, **kwargs):
        # Allow the response from the request to be passed in as a 'resp'
        # argument.
        self.resp = kwargs.pop('resp', None)
        super(UIError, self).__init__(*args, **kwargs)


class UIResponseError(UIError):
    """ An error raised when an unexpected error response was received from a
    server, prompting a message in a UI.
    """
    pass


class UIInputError(UIError):
    """ Some error related to missing/invalid form input."""
    pass


class FeatureMissingError(AttributeError):
    pass

class GuiError(UIError):
    pass


class GuiInputError(GuiError, UIInputError):
    pass


class SeleniumError(WebDriverException):
    """
    Exception thrown after receiving an error from the Selenium server.
    """
    pass


# Don't preserve the Java stacktrace garbage.  It's not useful to us.
_old_webdriverexception_init = WebDriverException.__init__
def _webdriverexception_init(self, *args, **kwargs):
    _old_webdriverexception_init(self, *args, **kwargs)
    self.stacktrace = None
WebDriverException.__init__ = _webdriverexception_init
