from werkzeug.wrappers import Request, Response


class authenticate():
    '''
    Autheticate request using token
    '''

    def __init__(self, app, token):
        self.app = app
        self.token = token

    def __call__(self, environ, start_response):
        request = Request(environ)
        _token = request.headers['Authentication']

        if _token == self.token:
            return self.app(environ, start_response)

        response = Response(u'Authorization failed',
                            mimetype='text/plain', status=401)

        return response(environ, start_response)
