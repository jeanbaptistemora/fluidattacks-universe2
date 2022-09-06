# this is necessary because of pylint error thrown only in backend-async
# module about UPPER_CASE naming style with every variable declared here
# pylint: disable-all

from datetime import (
    datetime,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
)

Datetime = datetime

# Payloads
DynamoDelete = NamedTuple("DynamoDelete", [("Key", Dict[str, Any])])


SimplePayload = NamedTuple(
    "SimplePayload",
    [
        ("success", bool),
    ],
)
SimplePayloadMessage = NamedTuple(
    "SimplePayloadMessage",
    [
        ("success", bool),
        ("message", str),
    ],
)
UpdateAccessTokenPayload = NamedTuple(
    "UpdateAccessTokenPayload",
    [
        ("success", bool),
        ("session_jwt", str),
    ],
)

SignPostUrlsPayload = NamedTuple(
    "SignPostUrlsPayload", [("success", bool), ("url", Dict[str, Any])]
)


class Phone(NamedTuple):
    calling_country_code: str
    national_number: str
