# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityZeroRiskStatus,
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
    Dict,
    List,
)

LOGGER = logging.getLogger(__name__)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> VulnerabilitiesConnection:
    vulnerabilities_filters: Dict[str, Any] = vulnerabilities_filter(**kwargs)

    results = await search(
        after=kwargs.get("after"),
        exact_filters={"group_name": parent.name},
        must_filters=vulnerabilities_filters["must_filters"],
        must_not_filters=vulnerabilities_filters["must_not_filters"],
        index="vulnerabilities",
        limit=kwargs.get("first", 10),
        query=kwargs.get("search"),
    )

    loaders: Dataloaders = info.context.loaders
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


def vulnerabilities_filter(**kwargs: Any) -> Dict[str, Any]:
    vulns_must_filters: List[Dict[str, Any]] = must_filter(**kwargs)
    vulns_must_not_filters: List[Dict[str, Any]] = must_not_filter()

    if zero_risk := kwargs.get("zeroRisk"):
        vulns_must_filters.append({"zero_risk.status": zero_risk})
    else:
        vulns_must_not_filters.append(
            {"zero_risk.status": VulnerabilityZeroRiskStatus.REQUESTED}
        )

    filters: Dict[str, Any] = {
        "must_filters": vulns_must_filters,
        "must_not_filters": vulns_must_not_filters,
    }

    return filters


def must_filter(**kwargs: Any) -> List[Dict[str, Any]]:
    must_filters = []

    if treatment := kwargs.get("treatment"):
        must_filters.append({"treatment.status": str(treatment).upper()})

    if state := kwargs.get("stateStatus"):
        must_filters.append({"state.status": str(state).upper()})

    if verification := kwargs.get("verificationStatus"):
        must_filters.append({"verification.status": str(verification).upper()})

    return must_filters


def must_not_filter() -> List[Dict[str, Any]]:
    must_not_filters = [
        {"zero_risk.status": VulnerabilityZeroRiskStatus.CONFIRMED}
    ]

    return must_not_filters
