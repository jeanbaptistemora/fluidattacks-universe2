from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesRequest,
    VulnerabilitiesConnection,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Optional,
)


async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    after: Optional[str] = None,
    first: Optional[int] = None,
    **_kwargs: None,
) -> VulnerabilitiesConnection:
    loaders: Dataloaders = info.context.loaders
    return await loaders.finding_vulnerabilities_to_reattack_c.load(
        FindingVulnerabilitiesRequest(
            finding_id=parent.id,
            after=after,
            first=first,
            paginate=True,
        )
    )


def _must_filter(finding_id: str) -> list[dict[str, Any]]:
    must_filters: list[dict[str, Any]] = [
        {"findingId": finding_id},
        {"state.status": VulnerabilityStateStatus.VULNERABLE},
        {"verification.status": VulnerabilityVerificationStatus.REQUESTED},
    ]

    return must_filters
