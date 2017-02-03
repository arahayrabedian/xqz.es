#!/usr/bin/env python

from distutils.util import strtobool

from bottle import abort
from bottle import install
from bottle import post
from bottle import request
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

from wtforms import Form
from wtforms import validators
from wtforms.fields import StringField
from wtforms.fields import TextAreaField
from wtfnocaptcha.fields import NoCaptchaField

import settings

from decorators.slack_request_processor import slack_verification_preprocessor
from contact.views import contact
from oauth2.views import callback
from util import DictObject

route('/oauth2/callback/', 'GET', callback)
route('/contact/', ['GET', 'POST'], contact)

# set up sqlalchemy
AlchemyBase = declarative_base()

engine = create_engine(settings.DATABASE_CONNECTION_STRING, echo=True)
create_session = sessionmaker(bind=engine)

# set up the sqlalchemy plugin
sqlalchemy_plugin = sqlalchemy.Plugin(
        engine,
        AlchemyBase.metadata,
        keyword='db',
        create=True,
        commit=True,
        use_kwargs=False
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
        return db.query(cls).filter(
            cls.published==True
        ).order_by(
            func.random()
        ).first()


@post('/slacktion/')
@slack_verification_preprocessor
def process_slack_command(db):
    """Parse /commands and route them to their appropriate processing methods
    """

    # make our lives a little easier
    slack_data = DictObject(request.forms)

    # small chance text is empty (if a stupid dev is curling manually)
    if 'text' in slack_data.attributes.keys():
        # match help text
        if slack_data.text == 'help':
            return {
                "text": "Request this help text with `/xqzes help`\n"
                        "Request an excuse (visible to everyone) with `/xqzes`\n"
                        "Submit a new excuse to a moderator with "
                        "`/xqzes add <your text here>`\n"
                        "e.g: `/xqzes add I was shopping!`"
            }
        elif slack_data.text.startswith("add"):
            # here we want to add a new non-approved excuse
            excuse_text = slack_data.text.lstrip(" add ")
            if len(excuse_text) > 140:
                return {
                    'text': "We conform to twitter standards (for no particular "
                            "reason), please keep your excuses shorter than "
                            "140 characters"
                }
            excuse = Excuse(slack_data.user_name, excuse_text)
            excuse.team_id = slack_data.team_id
            db.add(excuse)
            return {
                'text': "Your excuse has been added to the moderation queue. This "
                        "can take anywhere from a few minutes to a few years"
            }

    try:
        excuse_text = Excuse.get_random_excuse(db).excuse
    except AttributeError:
        abort(404, "NO EXCUSE FOR YOU, but, maybe we need one :(")
    return {
        "response_type": "in_channel",
        "text": excuse_text,
    }


@route('/')
def hello(db):
    """Serve up a plaintext public excuse for the purposes of
    """
    try:
        excuse_text = Excuse.get_random_excuse(db).excuse
    except AttributeError:
        abort(404, "NO EXCUSE FOR YOU, but, maybe we need one :(")

    return template(
        'home',
        excuse_text=excuse_text,
        slack_client_id=settings.SLACK_OAUTH['client_id'],
        slack_command_scope=settings.SLACK_OAUTH['command_scope'],
        slack_installed=strtobool(request.GET.get('added_to_slack', 'false')),
    )


@route('/privacy/')
def privacy_policy(db):
    return static_file('privacy_policy.txt', root=settings.TEMPLATE_PATH)


@route('/slack_instructions/')
def slack_instructions(db):
    return template(
        'slack_instructions',
        slack_client_id=settings.SLACK_OAUTH['client_id'],
        slack_command_scope=settings.SLACK_OAUTH['command_scope'],
        slack_installed=strtobool(request.GET.get('added_to_slack', 'false')),
    )


@route('/submit/')
@post('/submit/')
def submit(db):

    # TODO: break this out along with others in to an excuses package.
    class SubmissionForm(Form):
        attribution_name = StringField('Your Name (for future attribution purposes)',
                                       [validators.InputRequired()])
        excuse = TextAreaField(
            'What\'s YOUR excuse !?!?',
            [
                validators.Length(
                    min=5,
                    max=140,
                    message="Please provide %(min)d - %(max)d "
                            "characters"),
            ]
        )
        nocaptcha = NoCaptchaField(
            public_key=settings.RECAPTCHA_SITE_KEY,
            private_key=settings.RECAPTCHA_SECRET_KEY,
            secure=True,
        )

    form = SubmissionForm(request.POST, nocaptcha={'ip_address': '127.0.0.1'})

    submitted = False
    if request.method == 'POST' and form.validate():
        excuse_record = Excuse(form.attribution_name.data,
                               form.excuse.data)
        db.add(excuse_record)
        submitted = True

    return template('submit', form=form, submitted=submitted)



@route('/acknowledgements/')
def privacy_policy(db):
    return template('acknowledgements')


@route('/static/<path:path>')
def callback(path):
    return static_file(path, root=settings.STATIC_PATH)


if __name__ == '__main__':
    run(host='127.0.0.1', port=8088, debug=False)
