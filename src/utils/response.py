from flask import Response


class CustomResponse(Response):
    def __init__(
        self,
        status : int = 200,
        data : dict = {},
        errors : list = [],
        debugError: dict = {}
    ):
        super(CustomResponse, self).__init__()
        self.status = status
        self.data = data
        self.errors = errors
        self.debugError = debugError
