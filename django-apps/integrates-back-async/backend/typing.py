# this is necessary because of pylint error thrown only in backend-async
# module about UPPER_CASE naming style with every variable declared here
# pylint: disable-all

from decimal import Decimal
from typing import List, Dict, Union, Set, NamedTuple


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
    List[str]
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
    None
]]
User = Dict[str, Union[
    str, bool,
    List[str],
    Set[str],
    Dict[str, object],
    None
]]
Alert = Dict[str, Union[
    int, str
]]
AddUserPayload = NamedTuple('AddUserPayload', [
    ('success', bool),
    ('email', str),
])
GrantUserAccessPayload = NamedTuple('GrantUserAccessPayload', [
    ('success', bool),
    ('granted_user', User),
])
RemoveUserAccessPayload = NamedTuple('RemoveUserAccessPayload', [
    ('success', bool),
    ('removed_email', str),
])
EditUserPayload = NamedTuple('EditUserPayload', [
    ('success', bool),
    ('modified_user', User),
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
DownloadFilePayload = NamedTuple('DownloadFilePayload', [
    ('success', bool),
    ('url', str),
])
