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
    _parent: dict[str, Any],
    _info: GraphQLResolveInfo,
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
        must_not_filters=[{"group_name": "narrabri"}, not_zero_requested],
        index="findings",
        limit=100,
    )

    return tuple(format_finding(result) for result in results.items)
