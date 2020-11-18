# this is necessary because of pylint error thrown only in backend-async
# module about UPPER_CASE naming style with every variable declared here
# pylint: disable-all

from datetime import datetime
from decimal import Decimal
from typing import Any, List, Dict, Union, Set, NamedTuple, Optional

from boto3.dynamodb.conditions import Key

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
DirectoryFilteringConfig = NamedTuple('DirectoryFilteringConfig', [
    ('paths', List[str]),
    ('policy', str)
])
IntegrationEnvironment = NamedTuple('IntegrationEnvironment', [
    ('kind', str),
    ('url', str)
])
GitRoot = NamedTuple('GitRoot', [
    ('branch', str),
    ('directory_filtering', Optional[DirectoryFilteringConfig]),
    ('environment', Optional[IntegrationEnvironment]),
    ('id', str),
    ('url', str)
])
IPRoot = NamedTuple('IPRoot', [
    ('address', str),
    ('id', str),
    ('port', int)
])
URLRoot = NamedTuple('URLRoot', [
    ('host', str),
    ('id', str),
    ('path', str),
    ('port', int),
    ('protocol', str)
])
Root = Union[GitRoot, IPRoot, URLRoot]
