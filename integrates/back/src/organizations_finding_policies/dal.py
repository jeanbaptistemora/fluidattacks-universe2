from dynamodb import (
    model,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
    OrgFindingPolicyState,
)


async def add_organization_finding_policy(
    finding_policy: OrgFindingPolicyItem,
) -> None:
    await model.add_organization_finding_policy(finding_policy=finding_policy)


async def update_finding_policy_status(
    *, org_name: str, finding_policy_id: str, status: OrgFindingPolicyState
) -> None:
    await model.update_organization_finding_policy_state(
        org_name=org_name, finding_policy_id=finding_policy_id, state=status
    )


async def remove_org_finding_policies(*, organization_name: str) -> None:
    await model.remove_org_finding_policies(
        organization_name=organization_name
    )
