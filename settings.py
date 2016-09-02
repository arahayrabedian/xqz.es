import os

from bottle import TEMPLATE_PATH as BOTTLE_TEMPLATE_PATH


DATABASE_CONNECTION_STRING = os.getenv("XQZES_DATABASE_CONNECTION_STRING",
                                       "sqlite:///excuses.sqlite")

# private token on slack to validate that it's slack making the request
SLACK_VERIFICATION_TOKEN = os.getenv('XQZES_SLACK_VERIFICATION_TOKEN', None)
SLACK_OAUTH = {
    'client_id': os.getenv('XQZES_SLACK_OAUTH_CLIENT_ID', None),
    'client_secret': os.getenv('XQZES_SLACK_OAUTH_CLIENT_SECRET', None),
    'token_url': 'https://slack.com/api/oauth.access',
    'command_scope': 'commands',
}

#  modify template path for production
TEMPLATE_PATH = os.getenv('XQZES_BOTTLE_TEMPLATE_PATH', './templates/')
BOTTLE_TEMPLATE_PATH.insert(0, TEMPLATE_PATH)
