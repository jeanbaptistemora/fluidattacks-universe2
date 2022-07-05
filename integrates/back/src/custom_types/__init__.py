# this is necessary because of pylint error thrown only in backend-async
# module about UPPER_CASE naming style with every variable declared here
# pylint: disable-all

from boto3.dynamodb.conditions import (
    ConditionBase,
)
from datetime import (
    datetime,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Union,
)
from typing_extensions import (
    TypedDict,
)

Action = NamedTuple(
    "Action",
    [
        ("action", str),
        ("date", str),
        ("justification", str),
        ("manager", str),
        ("times", int),
    ],
)
Datetime = datetime
Tracking = TypedDict(
    "Tracking",
    {
        "cycle": int,
        "open": int,
        "closed": int,
        "effectiveness": int,
        "date": str,
        "new": int,
        "in_progress": int,
        "accepted": int,
        "accepted_undefined": int,
        "assigned": str,
        "manager": str,
        "justification": str,
    },
    total=False,
)

# Analytics
GraphicParameters = NamedTuple(
    "GraphicParameters",
    [
        ("document_name", str),
        ("document_type", str),
        ("entity", str),
        ("generator_name", str),
        ("generator_type", str),
        ("height", int),
        ("subject", str),
        ("width", int),
    ],
)
GraphicsForEntityParameters = NamedTuple(
    "GraphicsForEntityParameters",
    [
        ("entity", str),
        ("subject", str),
    ],
)
ReportParameters = NamedTuple(
    "ReportParameters",
    [
        ("entity", str),
        ("subject", str),
    ],
)

# Payloads
AddConsultPayload = NamedTuple(
    "AddConsultPayload",
    [
        ("success", bool),
        ("comment_id", str),
    ],
)
AddStakeholderPayload = NamedTuple(
    "AddStakeholderPayload",
    [
        ("success", bool),
        ("email", str),
    ],
)


class AddDraftPayload(NamedTuple):
    draft_id: str
    success: bool


class AddRootPayload(NamedTuple):
    root_id: str
    success: bool


class AddEventPayload(NamedTuple):
    event_id: str
    success: bool


ApproveDraftPayload = NamedTuple(
    "ApproveDraftPayload",
    [
        ("success", bool),
        ("release_date", str),
    ],
)
DownloadFilePayload = NamedTuple(
    "DownloadFilePayload",
    [
        ("success", bool),
        ("url", str),
    ],
)
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
