# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.findings.types import (
    Finding,
)
from db_model.findings.utils import (
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
    _info: GraphQLResolveInfo,
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
        index="findings",
        limit=25,
    )
    return tuple(format_finding(finding) for finding in results.items)
