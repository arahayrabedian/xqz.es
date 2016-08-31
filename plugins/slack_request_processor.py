from bottle import request


class Slackbject(object):

    def __init__(self, attributes):
        self.attributes = attributes

    def __getattribute__(self, name):
        try:
            return self.attributes[name]
        except Exception:
            return object.__getattribute__(self, name)


def slack_data_extractor(callback):
    """
    Reduce boilerplate dict extraction in the code by extracting slack POST
    form data in to a nice little wrapping object that we can retrieve from:
    e.g: request.forms['text'] --> request.slack.text
    """
    def wrapper(*args, **kwargs):
        #TODO: find a condition for this to occur, not always.
        request.slack = Slackbject(request.forms)
        body = callback(*args, **kwargs)
        return body
    return wrapper
