"""Singer object interfaces"""

from collections.abc import (
    Callable,
)
import datetime
from typing import (
    Any,
    NamedTuple,
    TypeVar,
)

JSONschema = dict[str, Any]
JSONmap = dict[str, Any]
DateTime = datetime.datetime


class SingerSchema(NamedTuple):
    """Singer schema object type"""

    stream: str
    schema: JSONschema
    key_properties: frozenset[str]
    bookmark_properties: frozenset[str] | None = None


class SingerRecord(NamedTuple):
    """Singer record object type"""

    stream: str
    record: JSONmap
    time_extracted: DateTime | None = None


class SingerState(NamedTuple):
    """Singer state object type"""

    value: JSONmap


SingerMessage = SingerRecord | SingerSchema | SingerState
State = TypeVar("State")
SingerHandler = Callable[[str, State], State]


class MissingKeys(KeyError):
    pass


class InvalidType(ValueError):
    pass
