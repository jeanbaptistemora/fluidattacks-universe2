# Standard libraries
from typing import (
    Tuple,
)

# Local libraries
from dynamodb.types import (
    OrgFindingPolicyItem,
)
from .dal import (
    get_org_finding_policies,
)


async def get_finding_policies(
    *,
    org_name: str
) -> Tuple[OrgFindingPolicyItem, ...]:
    return await get_org_finding_policies(org_name=org_name)
