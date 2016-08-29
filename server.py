import os

from bottle import install
from bottle import post
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


class Excuse(AlchemyBase):

    __tablename__ = "excuses"
    id = Column(Integer, primary_key=True)
    excuse = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, default=False)

    def __init__(self, excuse):
        self.excuse = excuse

    def __repr__(self):
        return "{id}: {excuse}".format(id=self.id, excuse=self.excuse)

    @classmethod
    def get_random_excuse(cls, db):
        return db.query(cls).filter(
            cls.published == True
        ).order_by(
            func.random()
        ).first()

@post('/xqz-moi')
def make_an_excuse(db):
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
    try:
        excuse_text = Excuse.get_random_excuse(db).excuse
    except AttributeError:
        raise HTTPError(404, "NO EXCUSE FOR YOU (our db is empty lol)")
    html = "<center><H1>%s</H1></center>" % excuse_text
    return html


if __name__ == '__main__':
    run(host='127.0.0.1', port=8088, debug=False)