# pylint: disable=super-with-arguments
from __future__ import (
    annotations,
)


class CustomBaseException(Exception):
    pass


class _SingleMessageException(CustomBaseException):
    msg: str

    @classmethod
    def new(cls) -> _SingleMessageException:
        return cls(cls.msg)


class UnavailabilityError(_SingleMessageException):
    msg: str = "AWS service unavailable, please retry"


class InvalidFilterCursor(CustomBaseException):
    """Exception to control the cursor with filters"""

    def __init__(self) -> None:
        msg = "Exception - The cursor is invalid with a filter"
        super(InvalidFilterCursor, self).__init__(msg)
