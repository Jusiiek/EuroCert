from typing import Any


class EuroCertException(Exception):
    pass


class UserAlreadyExists(EuroCertException):
    pass


class InvalidID(EuroCertException):
    pass


class UserNotExists(EuroCertException):
    pass


class InvalidPasswordException(EuroCertException):
    def __init__(self, reason: Any) -> None:
        self.reason = reason
