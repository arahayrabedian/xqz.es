import datetime

from random import choice

from bottle import post
from bottle import route
from bottle import run


EXCUSES = [
    "I went to return the rental!",
    "Unfortunately, I already set up an appointment with my instructor",
    "I didn't hang my laundry last night",
    "I was hungry",
    "I overslept",
    "I forgot",
    "I'm going for a beer",
    "My phone was on silent",
    "I just did my hair",
    "I slept funny",
    "My back hurts",
    "friggin neighbor has the stereo on all night",
]


@post('/xqz-moi')
def make_an_excuse():
    return {
        "response_type": "in_channel",
        "text": choice(EXCUSES),
    }


@route('/')
def hello():
    excuse = choice(EXCUSES)
    html = "<center><H1>%s</H1></center>" % excuse
    return html


run(host='127.0.0.1', port=8088, debug=False)
