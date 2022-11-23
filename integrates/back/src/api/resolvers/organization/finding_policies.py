# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model.organization_finding_policies.types import (
    OrgFindingPolicy,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
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
    finding_policies: tuple[OrgFindingPolicy, ...]
) -> tuple[OrgFindingPolicyApi, ...]:
    return tuple(
        OrgFindingPolicyApi(
            id=policy.id,
            last_status_update=datetime_utils.get_datetime_from_iso_str(
                policy.state.modified_date
            ),
            name=policy.name,
            status=policy.state.status.value,
            tags=set(policy.tags),
        )
        for policy in finding_policies
    )


async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[OrgFindingPolicyApi, ...]:
    loaders: Dataloaders = info.context.loaders
    finding_policies = await loaders.organization_finding_policies.load(
        parent.name
    )

    return _format_policies_for_resolver(finding_policies)
