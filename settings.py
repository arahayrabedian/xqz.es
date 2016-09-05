import os

from bottle import TEMPLATE_PATH as BOTTLE_TEMPLATE_PATH


DATABASE_CONNECTION_STRING = os.getenv("XQZES_DATABASE_CONNECTION_STRING",
                                       "sqlite:///excuses.sqlite")

# Email sending credentials
ADMIN_EMAIL = os.getenv('XQZES_ADMIN_EMAIL')
ADMIN_EMAIL_PASSWORD = os.getenv('XQZES_ADMIN_EMAIL_PASSWORD')


# private token on slack to validate that it's slack making the request
SLACK_VERIFICATION_TOKEN = os.getenv('XQZES_SLACK_VERIFICATION_TOKEN')
SLACK_OAUTH = {
    'client_id': os.getenv('XQZES_SLACK_OAUTH_CLIENT_ID'),
    'client_secret': os.getenv('XQZES_SLACK_OAUTH_CLIENT_SECRET'),
    'token_url': 'https://slack.com/api/oauth.access',
    'command_scope': 'commands',
}

# recaptcha credentials
RECAPTCHA_SITE_KEY = os.getenv('XQZES_RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = os.getenv('XQZES_RECAPTCHA_SECRET_KEY')

# modify template path for production
TEMPLATE_PATH = os.getenv('XQZES_BOTTLE_TEMPLATE_PATH', './templates/')
BOTTLE_TEMPLATE_PATH.insert(0, TEMPLATE_PATH)
