from distutils.util import strtobool

from gmail import GMail
from gmail import Message

from bottle import redirect
from bottle import request
from bottle import template

import settings

from contact.forms import ContactForm


def contact(db):
    """
    Our contact-us form, basically, present a form if it's a GET request,
    validate and process the form if it's a POST request. Filthy but works.
    """
    form = ContactForm(request.POST, recaptcha={'ip_address': '127.0.0.1'})
    if request.method == 'POST' and form.validate():
        # process the form, captcha is valid.

        message_text = "Contact Email: {email}\n\n {contact_text}".format(
            email=form.email.data,
            contact_text=form.contact_text.data
        )

        # put together a gmail client for sending messages
        gmail_client = GMail(settings.ADMIN_EMAIL,
                             settings.ADMIN_EMAIL_PASSWORD)
        message = Message('[xqzes] Contact Form',
                          to=settings.ADMIN_EMAIL,
                          text=message_text)
        gmail_client.send(message)

        return redirect("/contact/?contacted=True")

    return template(
        'contact',
        form=form,
        contacted=strtobool(request.GET.get('contacted', 'false'))
    )
