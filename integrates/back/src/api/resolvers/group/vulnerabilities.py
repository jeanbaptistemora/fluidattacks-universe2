from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
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
TREATMENTS = ["ACCEPTED", "ACCEPTED_UNDEFINED", "IN_PROGRESS"]


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
        must_match_prefix_filters=vulnerabilities_filters[
            "must_match_filters"
        ],
        must_not_filters=vulnerabilities_filters["must_not_filters"],
        index="vulnerabilities",
        limit=kwargs.get("first", 10),
        query=kwargs.get("search"),
        should_filters=vulnerabilities_filters["should_filters"],
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
    vulns_must_match_prefix_filters: List[
        Dict[str, Any]
    ] = must_match_prefix_filter(**kwargs)
    vulns_must_not_filters: List[Dict[str, Any]] = must_not_filter(**kwargs)
    vulns_should_filters: List[Dict[str, Any]] = should_filter(**kwargs)

    if zero_risk := kwargs.get("zeroRisk"):
        vulns_must_filters.append({"zero_risk.status": zero_risk})
    else:
        vulns_must_not_filters.append(
            {"zero_risk.status": VulnerabilityZeroRiskStatus.REQUESTED}
        )

    filters: Dict[str, Any] = {
        "must_filters": vulns_must_filters,
        "must_match_filters": vulns_must_match_prefix_filters,
        "must_not_filters": vulns_must_not_filters,
        "should_filters": vulns_should_filters,
    }

    return filters


def must_filter(**kwargs: Any) -> List[Dict[str, Any]]:
    must_filters = []

    if vulnerability_type := kwargs.get("type"):
        must_filters.append({"type": str(vulnerability_type).upper()})

    if verification := kwargs.get("verificationStatus"):
        must_filters.append({"verification.status": str(verification).upper()})

    return must_filters


def must_match_prefix_filter(**kwargs: Any) -> List[Dict[str, Any]]:
    must_match_filters = []

    if root := kwargs.get("root"):
        must_match_filters.append({"state.where": str(root).upper()})

    return must_match_filters


def must_not_filter(**kwargs: Any) -> list[dict[str, Any]]:
    must_not_filters: list[dict[str, Any]] = [
        {"state.status": VulnerabilityStateStatus.DELETED},
        {"state.status": VulnerabilityStateStatus.MASKED},
        {"state.status": VulnerabilityStateStatus.REJECTED},
        {"state.status": VulnerabilityStateStatus.SUBMITTED},
        {"zero_risk.status": VulnerabilityZeroRiskStatus.CONFIRMED},
    ]
    if treatment := kwargs.get("treatment"):
        if str(treatment).upper() in {"NEW", "UNTREATED"}:
            must_not_filters.extend(
                [{"treatment.status": treat} for treat in TREATMENTS]
            )
        else:
            must_not_filters.append({"treatment.status": "NEW"})
            must_not_filters.append({"treatment.status": "UNTREATED"})
            must_not_filters.extend(
                [
                    {"treatment.status": treat}
                    for treat in TREATMENTS
                    if treat != str(treatment).upper()
                ]
            )

    if state := kwargs.get("stateStatus"):
        if str(state).upper() in {"OPEN", "VULNERABLE"}:
            must_not_filters.append({"state.status": "CLOSED"})
            must_not_filters.append({"state.status": "SAFE"})
        else:
            must_not_filters.append({"state.status": "OPEN"})
            must_not_filters.append({"state.status": "VULNERABLE"})

    return must_not_filters


def should_filter(**kwargs: Any) -> List[Dict[str, Any]]:
    should_filters = []

    if state := kwargs.get("stateStatus"):
        if str(state).upper() in {"OPEN", "VULNERABLE"}:
            should_filters.append({"state.status": "OPEN"})
            should_filters.append({"state.status": "VULNERABLE"})
        else:
            should_filters.append({"state.status": "CLOSED"})
            should_filters.append({"state.status": "SAFE"})

    if treatment := kwargs.get("treatment"):
        if str(treatment).upper() in {"NEW", "UNTREATED"}:
            should_filters.append({"treatment.status": "NEW"})
            should_filters.append({"treatment.status": "UNTREATED"})
        else:
            should_filters.append({"treatment.status": str(treatment).upper()})

    return should_filters
