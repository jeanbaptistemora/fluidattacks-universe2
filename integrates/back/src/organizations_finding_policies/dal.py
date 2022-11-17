# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dynamodb import (
    model,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
    OrgFindingPolicyState,
)
from typing import (
    Optional,
    Tuple,
)


async def get_organization_finding_policies(
    *, org_name: str
) -> Tuple[OrgFindingPolicyItem, ...]:
    return await model.get_org_finding_policies(org_name=org_name)


async def get_organization_finding_policy(
    *,
    org_name: str,
    finding_policy_id: str,
) -> Optional[OrgFindingPolicyItem]:
    return await model.get_org_finding_policy(
        org_name=org_name, finding_policy_id=finding_policy_id
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
