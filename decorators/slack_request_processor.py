from bottle import abort
from bottle import request

import settings


def slack_verification_preprocessor(view):
    """
    Reduce boilerplate dict extraction in the code by extracting slack POST
    form data in to a nice little wrapping object that we can retrieve from:
    e.g: request.forms['text'] --> request.slack.text
    """
    def wrapper(db, *args, **kwargs):
        try:
            assert('token' in request.forms)
        except AssertionError:
            abort(400, "No token provided to authenticate")

        try:
            assert(request.forms['token'] == settings.SLACK_VERIFICATION_TOKEN)
        except AssertionError:
            abort(401, "Do you even authenticate, bro?")

        body = view(db, *args, **kwargs)
        return body

    return wrapper
