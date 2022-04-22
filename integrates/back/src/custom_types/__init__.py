# this is necessary because of pylint error thrown only in backend-async
# module about UPPER_CASE naming style with every variable declared here
# pylint: disable-all

from boto3.dynamodb.conditions import (
    ConditionBase,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Set,
    Union,
)
from typing_extensions import (
    TypedDict,
)

Comment = Dict[str, Any]
DynamoQuery = Dict[str, Union[ConditionBase, str]]
Evidence = Dict[str, Dict[str, str]]
ExploitResult = Dict[str, str]
Historic = List[Dict[str, str]]
InternalName = Dict[str, str]
Invitation = Dict[str, Union[str, bool]]
MailContent = Dict[str, Union[int, str, List[Dict[str, str]], Iterable[str]]]
Organization = Dict[str, Any]
Group = Dict[
    str, Union[str, object, List[Dict[str, str]], List[str], Set[str]]
]
Report = Dict[str, bool]
Stakeholder = Dict[
    str, Union[bool, str, Dict[str, object], List[str], Set[str], None]
]
Tag = Dict[str, Union[Decimal, str, List[str]]]
User = Dict[str, Any]

Dynamo = Union[str, Organization]
Event = Dict[str, Any]
ExecutionVulnerabilities = Dict[str, Union[int, List[ExploitResult]]]
ForcesExecution = Dict[str, Union[str, datetime, ExecutionVulnerabilities]]
ForcesExecutions = Dict[str, Union[datetime, str, List[ForcesExecution], None]]
Me = Dict[str, Union[bool, str, List[Union[Group, Tag, str]]]]
GroupAccess = Dict[str, Union[bool, int, str, Invitation, None]]
SignedUrl = Dict[str, Dict[str, str]]

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
AddOrganizationPayload = NamedTuple(
    "AddOrganizationPayload",
    [("success", bool), ("organization", Organization)],
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
        ("modified_stakeholder", Stakeholder),
    ],
)
ExecuteMachinePayload = NamedTuple(
    "ExecuteMachinePayload",
    [
        ("success", bool),
        ("pipeline_url", str),
    ],
)
GrantStakeholderAccessPayload = NamedTuple(
    "GrantStakeholderAccessPayload",
    [
        ("success", bool),
        ("granted_stakeholder", Stakeholder),
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
        ("group", Group),
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
    "SignPostUrlsPayload", [("success", bool), ("url", SignedUrl)]
)


class Phone(NamedTuple):
    calling_country_code: str
    national_number: str


class StakeholderPhone(NamedTuple):
    country_code: str
    calling_country_code: str
    national_number: str
