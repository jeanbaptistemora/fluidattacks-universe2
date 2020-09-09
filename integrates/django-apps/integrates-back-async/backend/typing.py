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
AddUserPayload = NamedTuple('AddUserPayload', [
    ('success', bool),
    ('email', str),
])
AddStakeholderPayload = NamedTuple('AddStakeholderPayload', [
    ('success', bool),
    ('email', str),
])
CreateOrganizationPayload = NamedTuple('CreateOrganizationPayload', [
    ('success', bool),
    ('organization', Organization)
])
GrantUserAccessPayload = NamedTuple('GrantUserAccessPayload', [
    ('success', bool),
    ('granted_user', User),
])
GrantStakeholderAccessPayload = NamedTuple('GrantStakeholderAccessPayload', [
    ('success', bool),
    ('granted_stakeholder', Stakeholder),
])
RemoveUserAccessPayload = NamedTuple('RemoveUserAccessPayload', [
    ('success', bool),
    ('removed_email', str),
])
RemoveStakeholderAccessPayload = NamedTuple('RemoveStakeholderAccessPayload', [
    ('success', bool),
    ('removed_email', str),
])
EditUserPayload = NamedTuple('EditUserPayload', [
    ('success', bool),
    ('modified_user', User),
])
EditStakeholderPayload = NamedTuple('EditStakeholderPayload', [
    ('success', bool),
    ('modified_stakeholder', User),
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
AddCommentPayload = NamedTuple('AddCommentPayload', [
    ('success', bool),
    ('comment_id', str),
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
