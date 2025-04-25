from typing import Any


class ClientErrorAPIException(Exception):
    """Исключение для HTTP code: (400..499]"""

    def __init__(self, status_code: int):
        self.status_code = status_code
        # self.body_json = body_json


class BadRequestAPIException(ClientErrorAPIException):
    """Исключение для HTTP code: 400"""


class ServerErrorAPIException(Exception):
    """Исключение для HTTP code: [500..)"""

    def __init__(self, status_code: int):
        self.status_code = status_code
        # self.body = body
