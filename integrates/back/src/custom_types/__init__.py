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

UpdateStakeholderPayload = NamedTuple(
    "UpdateStakeholderPayload",
    [
        ("success", bool),
        ("modified_stakeholder", Dict[str, Any]),
    ],
)
UpdateToeInputPayload = NamedTuple(
    "UpdateToeInputPayload",
    [
        ("component", str),
        ("entry_point", str),
        ("group_name", str),
        ("root_id", str),
        ("success", bool),
    ],
)
UpdateToeLinesPayload = NamedTuple(
    "UpdateToeLinesPayload",
    [
        ("filename", str),
        ("group_name", str),
        ("root_id", str),
        ("success", bool),
    ],
)
ExecuteMachinePayload = NamedTuple(
    "ExecuteMachinePayload",
    [
        ("success", bool),
        ("pipeline_url", str),
    ],
)

RemoveStakeholderAccessPayload = NamedTuple(
    "RemoveStakeholderAccessPayload",
    [
        ("success", bool),
        ("removed_email", str),
    ],
)
SignInPayload = NamedTuple(
    "SignInPayload",
    [
        ("success", bool),
        ("session_jwt", str),
    ],
)
SimpleFindingPayload = NamedTuple(
    "SimpleFindingPayload",
    [
        ("success", bool),
        ("finding", Dict[str, Any]),
    ],
)
SimpleGroupPayload = NamedTuple(
    "SimpleGroupPayload",
    [
        ("success", bool),
        ("group", dict[str, Any]),
    ],
)
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
