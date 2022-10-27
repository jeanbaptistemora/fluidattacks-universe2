# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.types import (
    VulnerabilitiesConnection,
    VulnerabilityEdge,
)
from db_model.vulnerabilities.utils import (
    format_vulnerability,
)
from graphql import (
    GraphQLResolveInfo,
)
import logging
from search.operations import (
    search,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> VulnerabilitiesConnection:
    after = kwargs.get("after")
    first = kwargs.get("first", 10)
    query = kwargs.get("search")

    must_filters = []
    if treatment := kwargs.get("treatment"):
        must_filters.append({"treatment.status": str(treatment).upper()})

    if state := kwargs.get("stateStatus"):
        must_filters.append({"state.status": str(state).upper()})

    if verification := kwargs.get("verificationStatus"):
        must_filters.append({"verification.status": str(verification).upper()})

    results = await search(
        after=after,
        exact_filters={"group_name": parent.name},
        must_filters=must_filters,
        must_not_filters=[{"zero_risk.status": "CONFIRMED"}],
        index="vulnerabilities",
        limit=first,
        query=query,
    )
    loaders = info.context.loaders
    draft_ids = tuple(
        draft.id for draft in await loaders.group_drafts.load(parent.name)
    )
    vulnerabilities = tuple(
        format_vulnerability(result) for result in results.items
    )

    return VulnerabilitiesConnection(
        edges=tuple(
            VulnerabilityEdge(
                cursor=results.page_info.end_cursor,
                node=vulnerability,
            )
            for vulnerability in vulnerabilities
            if vulnerability.finding_id not in draft_ids
        ),
        page_info=results.page_info,
        total=results.total,
    )
