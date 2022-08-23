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


class AdvisoryAlreadyCreated(_SingleMessageException):
    msg: str = "This advisory has already been created"


class UnavailabilityError(_SingleMessageException):
    msg: str = "AWS service unavailable, please retry"


class InvalidActionParameter(_SingleMessageException):
    msg: str = (
        "Invalid/Missing parameter. "
        "Insert a valid action (add | update | delete)"
    )


class InvalidScaPatchFormat(_SingleMessageException):
    msg: str = "Json file must contain an array with all involved advisories"


class InvalidPathParameter(_SingleMessageException):
    msg: str = "Invalid/Missing parameter. Insert a valid file path"


class InvalidPatchItem(_SingleMessageException):
    msg: str = (
        "Invalid item, "
        "if 'add/update' then all attributes except 'source' are required, "
        "if 'delete' then 'vulnerable_version', 'severity' are not required"
    )


class InvalidSeverity(_SingleMessageException):
    msg: str = (
        "Invalid 'severity' format, please check metrics for incorrect values"
    )


class InvalidVulnerableVersion(_SingleMessageException):
    msg: str = (
        "Invalid 'vulnerable_version' format, each range must start with "
        "('=' | '<' | '>' | '>=' | '<=')"
    )


class InvalidFilterCursor(CustomBaseException):
    """Exception to control the cursor with filters"""

    def __init__(self) -> None:
        msg = "Exception - The cursor is invalid with a filter"
        super(InvalidFilterCursor, self).__init__(msg)
