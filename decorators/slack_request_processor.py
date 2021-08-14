from bottle import abort
from bottle import request

import settings


def slack_verification_preprocessor(view):
    """
    Run some preliminary authentication - by Slack policy (and, given team
    privacy considerations), we need to ensure that requests legitimately
    come from slack. There is an assigned (secret) shared token that we need to
    compare from our side to the incoming request.

    we need to:
    1) ensure it is present (first assertion)
    2) ensure it matches (second assertion)

    if these two succeed, then we can allow the view to be called.
    """

    def wrapper(db, *args, **kwargs):
        try:
            assert "token" in request.forms
        except AssertionError:
            abort(400, "No token provided to authenticate")

        try:
            assert request.forms["token"] == settings.SLACK_VERIFICATION_TOKEN
        except AssertionError:
            abort(401, "Do you even authenticate, bro?")

        body = view(db, *args, **kwargs)
        return body

    return wrapper
