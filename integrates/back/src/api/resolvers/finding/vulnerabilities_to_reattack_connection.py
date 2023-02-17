from .schema import (
    FINDING,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    VulnerabilitiesConnection,
    VulnerabilityEdge,
)
from db_model.vulnerabilities.utils import (
    format_vulnerability,
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


@FINDING.field("vulnerabilitiesToReattackConnection")
async def resolve(
    parent: Finding,
    _info: GraphQLResolveInfo,
    **kwargs: Any,
) -> VulnerabilitiesConnection:
    vulns_must_filters: list[dict[str, Any]] = _must_filter(parent.id)

    results = await search(
        after=kwargs.get("after"),
        must_filters=vulns_must_filters,
        index="vulnerabilities",
        limit=kwargs.get("first", 1000),
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
        ),
        page_info=results.page_info,
        total=results.total,
    )


def _must_filter(finding_id: str) -> list[dict[str, Any]]:
    must_filters: list[dict[str, Any]] = [
        {"sk": f"FIN#{finding_id}"},
        {"state.status": VulnerabilityStateStatus.VULNERABLE},
        {"verification.status": VulnerabilityVerificationStatus.REQUESTED},
    ]

    return must_filters
