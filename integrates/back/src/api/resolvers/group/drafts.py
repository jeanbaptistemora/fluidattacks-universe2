# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.findings.enums import (
    FindingStateStatus,
)
from db_model.findings.types import (
    Finding,
)
from db_model.findings.utils import (
    filter_non_state_status_findings,
    format_finding,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from search.operations import (
    search,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Finding, ...]:
    group_name: str = parent.name
    results = await search(
        exact_filters={"group_name": group_name},
        index="findings",
        limit=50,
    )
    findings: tuple[Finding, ...] = tuple(
        format_finding(finding) for finding in results.items
    )
    return tuple(
        filter_non_state_status_findings(
            findings,
            {
                FindingStateStatus.APPROVED,
                FindingStateStatus.DELETED,
            },
        )
    )
