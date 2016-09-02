
class DictObject(object):
    """
    Reduce boilerplate dict extraction in the code by moving dicts in to
    nice little wrapping object that we can retrieve from:

    e.g: request.forms['text'] -->
    slack = DictObject(request.forms)
    slack.text
    """
    def __init__(self, attributes):
        self.attributes = attributes

    def __getattribute__(self, name):
        try:
            return self.attributes[name]
        except Exception:
            return object.__getattribute__(self, name)
