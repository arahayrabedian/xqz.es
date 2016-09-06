from wtforms import validators
from wtforms import StringField
from wtforms import Form
from wtforms import TextAreaField
from wtfnocaptcha.fields import NoCaptchaField

from settings import RECAPTCHA_SITE_KEY
from settings import RECAPTCHA_SECRET_KEY


class ContactForm(Form):
    email = StringField('Email Address',
                        [validators.Email()])
    contact_text = TextAreaField(
        'What the problem is?',
        [
            validators.Length(
                min=50,
                max=500,
                message="Please provide %(min)d - %(max)d "
                        "characters"),
        ]
    )
    nocaptcha = NoCaptchaField(
        public_key=RECAPTCHA_SITE_KEY,
        private_key=RECAPTCHA_SECRET_KEY,
        secure=True,
        # validator and error texts are already set in field.
    )
