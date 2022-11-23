"""Singer object interfaces"""

import datetime
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    NamedTuple,
    Optional,
    TypeVar,
    Union,
)

JSONschema = Dict[str, Any]
JSONmap = Dict[str, Any]
DateTime = datetime.datetime


class SingerSchema(NamedTuple):
    """Singer schema object type"""

    stream: str
    schema: JSONschema
    key_properties: FrozenSet[str]
    bookmark_properties: Optional[FrozenSet[str]] = None


class SingerRecord(NamedTuple):
    """Singer record object type"""

    stream: str
    record: JSONmap
    time_extracted: Optional[DateTime] = None


class SingerState(NamedTuple):
    """Singer state object type"""

    value: JSONmap


SingerMessage = Union[SingerRecord, SingerSchema, SingerState]
State = TypeVar("State")
SingerHandler = Callable[[str, State], State]


class MissingKeys(KeyError):
    pass


class InvalidType(ValueError):
    pass
