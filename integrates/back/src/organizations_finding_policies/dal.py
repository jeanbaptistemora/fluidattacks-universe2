from dynamodb import (
    model,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
)


async def add_organization_finding_policy(
    finding_policy: OrgFindingPolicyItem,
) -> None:
    await model.add_organization_finding_policy(finding_policy=finding_policy)


async def remove_org_finding_policies(*, organization_name: str) -> None:
    await model.remove_org_finding_policies(
        organization_name=organization_name
    )
