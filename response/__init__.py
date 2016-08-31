from bottle import HTTPResponse

class HTTPSlackResponse(HTTPResponse):
    def __init__(self, *args, **kwargs):
        super(HTTPSlackResponse, self).__init__(*args, **kwargs)

        # no assertion required, if we can't add the below, we fail hard.
        try:
            self.body["response_type"] = "in_channel"
        except:
            raise Exception("response type is not dict-y enough.")
