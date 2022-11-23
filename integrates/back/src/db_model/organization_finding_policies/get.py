# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .types import (
    OrgFindingPolicy,
    OrgFindingPolicyRequest,
)
from .utils import (
    format_organization_finding_policy,
)
from aiodataloader import (
    DataLoader,
)
from custom_exceptions import (
    OrgFindingPolicyNotFound,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_organization_finding_policy(
    *,
    requests: tuple[OrgFindingPolicyRequest, ...],
) -> tuple[OrgFindingPolicy, ...]:
    primary_keys = tuple(
        keys.build_key(
            facet=TABLE.facets["org_finding_policy_metadata"],
            values={
                "name": request.organization_name,
                "uuid": request.policy_id,
            },
        )
        for request in requests
    )
    items = await operations.batch_get_item(keys=primary_keys, table=TABLE)

    if len(items) == len(requests):
        response = {
            OrgFindingPolicyRequest(
                organization_name=policy.organization_name,
                policy_id=policy.id,
            ): policy
            for policy in tuple(
                format_organization_finding_policy(item) for item in items
            )
        }
        return tuple(response[request] for request in requests)

    raise OrgFindingPolicyNotFound()


class OrganizationFindingPolicyLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, requests: Iterable[OrgFindingPolicyRequest]
    ) -> tuple[OrgFindingPolicy, ...]:
        return await _get_organization_finding_policy(requests=tuple(requests))
