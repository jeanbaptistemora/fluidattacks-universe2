# this is necessary because of pylint error thrown only in backend-async
# module about UPPER_CASE naming style with every variable declared here
# pylint: disable-all

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, List, Dict, Union, Set, NamedTuple, Optional
from typing_extensions import TypedDict

from boto3.dynamodb.conditions import Key

Datetime = datetime
Tracking = TypedDict('Tracking', {
    'cycle': int,
    'open': int,
    'closed': int,
    'effectiveness': int,
    'date': str,
    'new': int,
    'in_progress': int,
    'accepted': int,
    'accepted_undefined': int,
    'manager': str,
}, total=False)
Historic = List[Dict[str, str]]
Evidence = Dict[str, Dict[str, str]]
Finding = Union[
    str, list, float,
    List[str], Dict[str, str],
    Historic, Evidence,
    Decimal,
    None
]
Project = Dict[str, Union[
    str, object,
    List[Dict[str, str]],
    List[str],
    Set[str]
]]
Organization = Dict[str, Union[
    Decimal,
    List[Dict[str, Union[Optional[Decimal], str]]],
    None,
    str
]]
Comment = Dict[str, Union[
    int, str, object
]]
Resource = Dict[str, Union[
    str, object,
    Historic
]]
Event = Dict[str, Union[
    str,
    Historic,
    List[Comment],
    None
]]
User = Dict[str, Union[
    str, bool,
    List[str],
    Set[str],
    Dict[str, object],
    None
]]
Stakeholder = Dict[str, Union[
    str, bool,
    List[str],
    Set[str],
    Dict[str, object],
    None
]]
Resources = Dict[str, Union[
    str,
    List[Resource]
]]
MailContent = Dict[str, Union[
    int, str,
    List[Dict[str, str]]
]]
Tag = Dict[str, Union[Decimal, str, List[str]]]
InternalName = Dict[str, str]
ExploitResult = Dict[str, str]
ExecutionVulnerabilities = Dict[str, Union[
    int,
    List[ExploitResult]
]]
ForcesExecution = Dict[str, Union[
    str,
    datetime,
    ExecutionVulnerabilities
]]
ForcesExecutions = Dict[str, Union[
    str,
    List[ForcesExecution],
    datetime,
    None
]]
Me = Dict[str, Union[
    str, bool,
    List[Union[Project, Tag, str]]
]]
Vulnerability = Dict[str, Union[
    str, bool,
    Historic,
    List[str]
]]
Report = Dict[str, Union[
    str
]]
AddStakeholderPayload = NamedTuple('AddStakeholderPayload', [
    ('success', bool),
    ('email', str),
])
CreateOrganizationPayload = NamedTuple('CreateOrganizationPayload', [
    ('success', bool),
    ('organization', Organization)
])

class OrganizationStakehodersPageSizeEnum(Enum):
    FIFTY: int = 50
    TEN: int = 10
    THIRTY: int = 30
    TWENTY: int = 20
    TWENTYFIVE: int = 25

GetOrganizationStakeholdersPayload = NamedTuple(
    'GetOrganizationStakeholdersPayload', [
        ('stakeholders', List[Stakeholder]),
        ('num_pages', int),
    ]
)
GrantStakeholderAccessPayload = NamedTuple('GrantStakeholderAccessPayload', [
    ('success', bool),
    ('granted_stakeholder', Stakeholder),
])
RemoveStakeholderAccessPayload = NamedTuple('RemoveStakeholderAccessPayload', [
    ('success', bool),
    ('removed_email', str),
])
EditStakeholderPayload = NamedTuple('EditStakeholderPayload', [
    ('success', bool),
    ('modified_stakeholder', Stakeholder),
])
SimplePayload = NamedTuple('SimplePayload', [
    ('success', bool),
])
SimpleFindingPayload = NamedTuple('SimpleFindingPayload', [
    ('success', bool),
    ('finding', Dict[str, Finding]),
])
ApproveDraftPayload = NamedTuple('ApproveDraftPayload', [
    ('success', bool),
    ('release_date', str),
])
AddConsultPayload = NamedTuple('AddConsultPayload', [
    ('success', bool),
    ('comment_id', str),
])
DownloadFilePayload = NamedTuple('DownloadFilePayload', [
    ('success', bool),
    ('url', str),
])
SimpleProjectPayload = NamedTuple('SimpleProjectPayload', [
    ('success', bool),
    ('project', Project),
])
SignInPayload = NamedTuple('SignInPayload', [
    ('success', bool),
    ('session_jwt', str),
])
UpdateAccessTokenPayload = NamedTuple('UpdateAccessTokenPayload', [
    ('success', bool),
    ('session_jwt', str),
])
Dynamo = Union[Organization, str]
DynamoQuery = Dict[str, Union[Key, str]]
DynamoDelete = NamedTuple(
    'DynamoDelete',
    [('Key', Dict[str, Any])]
)
ExecuteSkimsPayload = NamedTuple('ExecuteSkimsPayload', [
    ('success', bool),
    ('pipeline_url', str),
])
IntegrationEnvironment = NamedTuple(
    'IntegrationEnvironment',
    [
        ('kind', str),
        ('url', Optional[str])
    ]
)

GitRootCloningStatus = NamedTuple(
    'GitRootCloningStatus',
    [
        ('status', str),
        ('message', str),
    ],
)

GitRoot = NamedTuple(
    'GitRoot',
    [
        ('branch', str),
        ('cloning_status', GitRootCloningStatus),
        ('environment', str),
        ('environment_urls', List[str]),
        ('gitignore', List[str]),
        ('id', str),
        ('includes_health_check', bool),
        ('state', str),
        ('url', str)
    ]
)
IPRoot = NamedTuple(
    'IPRoot',
    [
        ('address', str),
        ('id', str),
        ('port', int)
    ]
)
URLRoot = NamedTuple(
    'URLRoot',
    [
        ('host', str),
        ('id', str),
        ('path', str),
        ('port', int),
        ('protocol', str)
    ]
)
Root = Union[GitRoot, IPRoot, URLRoot]

# Analytics
GraphicParameters = NamedTuple(
    'GraphicParameters',
    [
        ('document_name', str),
        ('document_type', str),
        ('entity', str),
        ('generator_name', str),
        ('generator_type', str),
        ('height', int),
        ('subject', str),
        ('width', int)
    ]
)
GraphicsForEntityParameters = NamedTuple(
    'GraphicsForEntityParameters',
    [
        ('entity', str),
        ('subject', str),
    ]
)
ReportParameters = NamedTuple(
    'ReportParameters',
    [
        ('entity', str),
        ('subject', str),
    ]
)
