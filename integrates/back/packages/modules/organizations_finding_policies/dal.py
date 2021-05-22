from typing import (
    Optional,
    Tuple,
)

from dynamodb import model
from dynamodb.types import (
    OrgFindingPolicyItem,
    OrgFindingPolicyState,
)


async def get_org_finding_policies(
    *, org_name: str
) -> Tuple[OrgFindingPolicyItem, ...]:
    return await model.get_org_finding_policies(org_name=org_name)


async def get_org_finding_policy(
    *,
    org_name: str,
    finding_policy_id: str,
) -> Optional[OrgFindingPolicyItem]:
    return await model.get_org_finding_policy(
        org_name=org_name, finding_policy_id=finding_policy_id
    )


async def add_org_finding_policy(finding_policy: OrgFindingPolicyItem) -> None:
    await model.create_org_finding_policy(finding_policy=finding_policy)


async def update_finding_policy_status(
    *, org_name: str, finding_policy_id: str, status: OrgFindingPolicyState
) -> None:
    await model.update_org_finding_policy_state(
        org_name=org_name, finding_policy_id=finding_policy_id, state=status
    )
