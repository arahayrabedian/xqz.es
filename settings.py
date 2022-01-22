import os

from bottle import TEMPLATE_PATH as BOTTLE_TEMPLATE_PATH


DATABASE_CONNECTION_STRING = os.getenv(
    "XQZES_DATABASE_CONNECTION_STRING", "sqlite:///excuses.sqlite"
)


# modify template path for production
STATIC_PATH = os.getenv("XQZES_BOTTLE_STATIC_PATH", "./media/")
TEMPLATE_PATH = os.getenv("XQZES_BOTTLE_TEMPLATE_PATH", "./templates/")
BOTTLE_TEMPLATE_PATH.insert(0, TEMPLATE_PATH)
