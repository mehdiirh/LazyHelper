class Error(Exception):

    code = ''
    message = ''

    def __init__(self, code=None, message='', **kwargs):
        if not message:
            self.message = self.message
        else:
            self.message = message

        if code is None:
            self.code = self.code
        else:
            self.code = code

        super().__init__(self.message)


class AuthenticationError(Error):
    code = 403
    message = 'Authentication failed'
