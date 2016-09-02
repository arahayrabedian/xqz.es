
class DictObject(object):

    def __init__(self, attributes):
        self.attributes = attributes

    def __getattribute__(self, name):
        try:
            return self.attributes[name]
        except Exception:
            return object.__getattribute__(self, name)
