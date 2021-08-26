from requests_oauthlib import OAuth2Session

from bottle import route
from bottle import redirect
from bottle import request

import settings

"""
Views we use for anything oauth2. This entire process is initialized by
someone clicking the "Add To Slack" button, at which point they start
the oauth2 process on the slack side. The first we hear of it is the callback.
"""


@route("/oauth2/callback/")
def callback():
    """ Step 3: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.

    NOTE: your server name must be correctly configured in order for this to
    work, do this by adding the headers at your http layer, in particular:
    X_FORWARDED_HOST, X_FORWARDED_PROTO so that bottle can render the correct
    url and links for you.
    """
    oauth2session = OAuth2Session(
        settings.SLACK_OAUTH["client_id"], state=request.GET["state"]
    )

    # PII - update privacy policy if oauth2 token is stored.
    token = oauth2session.fetch_token(
        settings.SLACK_OAUTH["token_url"],
        client_secret=settings.SLACK_OAUTH["client_secret"],
        authorization_response=request.url,
    )

    # we don't need the token, we just need the user to have installed the app
    # in the future, if we need tokens, we'll get them.

    redirect("/?added_to_slack=true")
