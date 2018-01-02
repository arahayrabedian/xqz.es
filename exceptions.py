

class CertificateValidationException(Exception):
    """
    Exception to be used when there is an issue with certificate validation,
    namely related to amazon/alexa support.
    """
    pass


class NotConfiguredError(Exception):
    """
    Exception to be used when something has been called without it being
    configured.
    """
    pass


class NotForMeError(Exception):
    """
    Error to use when a request comes in, but it's not really for you.
    """
    pass
