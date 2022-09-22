# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.findings.utils import (
    filter_non_in_test_orgs,
    format_finding,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from search.operations import (
    search,
)
from typing import (
    Any,
)


@require_login
async def resolve(
    _parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Finding, ...]:

    not_zero_requested = {
        "unreliable_indicators.unreliable_verification_summary.requested": 0
    }
    results = await search(
        must_filters=[
            {"verification.status": "REQUESTED"},
            {"unreliable_indicators.unreliable_status": "OPEN"},
        ],
        must_not_filters=[not_zero_requested],
        index="findings",
        limit=100,
    )

    loaders: Dataloaders = info.context.loaders
    test_group_orgs = await loaders.organization_groups.load_many(
        (
            "0d6d8f9d-3814-48f8-ba2c-f4fb9f8d4ffa",
            "a23457e2-f81f-44a2-867f-230082af676c",
        )
    )

    return filter_non_in_test_orgs(
        test_group_orgs,
        tuple(format_finding(result) for result in results.items),
    )
