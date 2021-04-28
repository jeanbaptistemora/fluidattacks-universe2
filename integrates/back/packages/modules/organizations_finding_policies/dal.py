# Standard library
from typing import (
    Tuple,
)

# Local libraries
from dynamodb import model
from dynamodb.types import (
    OrgFindingPolicyItem,
)


async def get_org_finding_policies(
    *,
    org_name: str
) -> Tuple[OrgFindingPolicyItem, ...]:
    return await model.get_org_finding_policies(org_name=org_name)


async def add_org_finding_policy(
    finding_policy: OrgFindingPolicyItem
) -> None:
    await model.create_org_finding_policy(finding_policy=finding_policy)
