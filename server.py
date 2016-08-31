import os

from bottle import install
from bottle import post
from bottle import request
from bottle import route
from bottle import run
from bottle.ext import sqlalchemy
from bottle import HTTPError

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from plugins.slack_request_processor import slack_data_extractor

# set up sqlalchemy
AlchemyBase = declarative_base()
db_url = os.getenv("XQZMOI_DATABASE_CONNECTION_STRING",
                   "sqlite:///excuses.sqlite")
engine = create_engine(db_url, echo=True)
create_session = sessionmaker(bind=engine)

# set up the sqlalchemy plugin
plugin = sqlalchemy.Plugin(
        engine,
        AlchemyBase.metadata,
        keyword='db',
        create=True,
        commit=True,
        use_kwargs=False
)

# set up the bottle app
install(plugin)
install(slack_data_extractor)


class Excuse(AlchemyBase):

    __tablename__ = "excuses"
    id = Column(Integer, primary_key=True)
    excuse = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, default=False)
    username = Column(String, nullable=False, default="admin")
    team_id = Column(String, nullable=True, default=None)

    def __init__(self, username, excuse):
        self.username = username
        self.excuse = excuse

    def __repr__(self):
        return "{id}: {excuse}".format(id=self.id, excuse=self.excuse)

    @classmethod
    def get_random_excuse(cls, db):
        return db.query(cls).filter(
            cls.published==True
        ).order_by(
            func.random()
        ).first()


@post('/slacktion/')
def process_slack_command(db):
    """Parse /commands and route them to their appropriate processing methods
    """

    # match help text
    if request.slack.text == 'help':
        return {
            "text": "so you want some help do you?"
        }
    elif request.slack.text.startswith("add"):
        # here we want to add a new non-approved excuse
        excuse_text = request.slack.text.lstrip(" add ")
        if len(excuse_text) > 140:
            return {
                'text': "We conform to twitter standards (for no particular "
                        "reason), please keep your excuses shorter than "
                        "140 characters"
            }
        excuse = Excuse(request.slack.user_name, excuse_text)
        excuse.team_id = request.slack.team_id
        db.add(excuse)
        return {
            'text': "Your excuse has been added to the moderation queue. This "
                    "can take anywhere from a few minutes to a few years"
        }

    try:
        excuse_text = Excuse.get_random_excuse(db).excuse
    except AttributeError:
        raise HTTPError(404, "NO EXCUSE FOR YOU (our db is empty lol)")
    return {
        "response_type": "in_channel",
        "text": excuse_text,
    }


@route('/')
def hello(db):
    """Serve up a plaintext public excuse for the purposes of
    :param db:
    :return:
    """
    try:
        excuse_text = Excuse.get_random_excuse(db).excuse
    except AttributeError:
        raise HTTPError(404, "NO EXCUSE FOR YOU (our db is empty? lol)")
    html = "<center><H1>%s</H1></center>" % excuse_text
    return html


if __name__ == '__main__':
    run(host='127.0.0.1', port=8088, debug=False)
