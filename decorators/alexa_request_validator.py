from bottle import abort
from bottle import request

from exceptions import CertificateValidationException
from exceptions import NotConfiguredError
from exceptions import NotForMeError
from util.alexa import validate_alexa_request


def alexa_request_validator(view):
    """
    Run alexa requests through a battery of required checks and balances
    """
    def wrapper(db, *args, **kwargs):
        try:
            raw_body_text = request.body.read().decode()
            validate_alexa_request(request.headers, raw_body_text)
        except CertificateValidationException as e:
            abort(400, "Request not issued by Amazon Alexa: %s" % str(e))
        except NotForMeError as e:
            abort(403, "Request valid, but not for this alexa skill")
        except NotConfiguredError as e:
            # I don't think unauthed is really correct, it's just not set up
            # therefore, we can 404 it, but say why.
            abort(404, "Alexa skills backend not configured on this server")

        return view(db, *args, **kwargs)

    return wrapper
