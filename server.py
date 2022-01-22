#!/usr/bin/env python


from bottle import abort
from bottle import install
from bottle import route
from bottle import run
from bottle import static_file
from bottle.ext import sqlalchemy
from bottle import template

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

import settings

# set up sqlalchemy
AlchemyBase = declarative_base()

engine = create_engine(settings.DATABASE_CONNECTION_STRING, echo=True)
create_session = sessionmaker(bind=engine)

# set up the sqlalchemy plugin
sqlalchemy_plugin = sqlalchemy.Plugin(
    engine,
    AlchemyBase.metadata,
    keyword="db",
    create=True,
    commit=True,
    use_kwargs=False,
)

# set up the bottle app
install(sqlalchemy_plugin)


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
        return (
            db.query(cls).filter(cls.published == True).order_by(func.random()).first()
        )


@route("/")
def hello(db):
    """Serve up a plaintext public excuse for the purposes of
    """
    try:
        excuse_text = Excuse.get_random_excuse(db).excuse
    except AttributeError:
        abort(404, "NO EXCUSE FOR YOU, but, maybe we need one :(")

    return template(
        "home",
        excuse_text=excuse_text,
    )


@route("/submit/")
def submit(db):
    return template("submit")


@route("/contact/")
def contact(db):
    return template("contact")


@route("/acknowledgements/")
def privacy_policy(db):
    return template("acknowledgements")


@route("/static/<path:path>")
def callback(path):
    return static_file(path, root=settings.STATIC_PATH)


if __name__ == "__main__":
    run(host="127.0.0.1", port=8088, debug=False)
