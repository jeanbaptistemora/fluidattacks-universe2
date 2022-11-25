from .enums import (
    PolicyStateStatus,
)
from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
)


class OrgFindingPolicyState(NamedTuple):
    modified_by: str
    modified_date: datetime
    status: PolicyStateStatus


class OrgFindingPolicy(NamedTuple):
    id: str
    name: str
    organization_name: str
    state: OrgFindingPolicyState
    tags: set[str]


class OrgFindingPolicyRequest(NamedTuple):
    organization_name: str
    policy_id: str
