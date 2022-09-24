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
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[Finding, ...]:
    user_email = str(parent["user_email"])
    results = await search(
        should_filters=[
            {"state.status": "CREATED"},
            {"state.status": "REJECTED"},
            {"state.status": "SUBMITTED"},
        ],
        must_filters=[{"analyst_email": user_email}],
        must_not_filters=[
            {"state.status": "APPROVED"},
            {"state.status": "DELETED"},
            {"state.status": "MASKED"},
        ],
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
