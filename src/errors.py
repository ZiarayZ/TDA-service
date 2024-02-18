import werkzeug


class InternalServerError(werkzeug.exceptions.HTTPException):
    code = 500
    description = "Internal Server Error"

    def __init__(self, desc: object):
        self.description = desc
