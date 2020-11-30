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

        def authenticated_response(status, headers, exc_info=None):
            headers.append(('Authentication', self.token))
            return start_response(status, headers, exc_info)

        if request.headers['Authentication'] == self.token:
            return self.app(environ, authenticated_response)

        response = Response(u'Authentication failed', status=401)

        return response(environ, start_response)
