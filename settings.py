import os

DATABASE_CONNECTION_STRING = os.getenv("XQZES_DATABASE_CONNECTION_STRING",
                                       "sqlite:///excuses.sqlite")

SLACK_OAUTH = {
    'client_id': os.getenv('SLACK_OAUTH_CLIENT_ID', None),
    'client_secret': os.getenv('SLACK_OAUTH_CLIENT_SECRET', None),
    'token_url': 'https://slack.com/api/oauth.access',
    'command_scope': 'commands',
}
