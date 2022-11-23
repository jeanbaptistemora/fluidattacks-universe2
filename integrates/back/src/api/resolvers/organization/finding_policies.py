# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from db_model.organizations.types import (
    Organization,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations_finding_policies.domain import (
    get_finding_policies,
)
from typing import (
    NamedTuple,
)


class OrgFindingPolicyApi(NamedTuple):
    id: str
    last_status_update: datetime
    name: str
    status: str
    tags: set[str]


def _format_policies_for_resolver(
    finding_policies: tuple[OrgFindingPolicyItem, ...]
) -> tuple[OrgFindingPolicyApi, ...]:
    return tuple(
        OrgFindingPolicyApi(
            id=policy.id,
            last_status_update=datetime_utils.get_datetime_from_iso_str(
                policy.state.modified_date
            ),
            name=policy.metadata.name,
            status=policy.state.status,
            tags=set(policy.metadata.tags),
        )
        for policy in finding_policies
    )


async def resolve(
    parent: Organization,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[OrgFindingPolicyApi, ...]:
    finding_policies = await get_finding_policies(org_name=parent.name)

    return _format_policies_for_resolver(finding_policies)
