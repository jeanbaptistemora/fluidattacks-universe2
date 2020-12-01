"""Singer object interfaces"""
# Standard libraries
import datetime
from typing import (
    Any,
    Dict,
    FrozenSet,
    NamedTuple,
    Optional,
    Union,
)
# Third party libraries
# Local libraries


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


SingerMessage = Union[SingerRecord, SingerSchema]


class MissingKeys(KeyError):
    pass


class InvalidType(ValueError):
    pass
