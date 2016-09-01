import os


DATABASE_CONNECTION_STRING = os.getenv("XQZMOI_DATABASE_CONNECTION_STRING",
                                       "sqlite:///excuses.sqlite")

SLACK_OAUTH = {
    'client_id': os.getenv('SLACK_OAUTH_CLIENT_ID', None),
    'command_scope': 'commands',
}
