# Standard
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
from backend.domain import (
    finding as finding_domain,
    vulnerability as vuln_domain,
)
from backend.typing import Finding, Vulnerability
from backend.filters import finding as finding_filters


@get_entity_cache_async
async def resolve(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> int:
    finding_id: str = cast(str, parent['id'])
    release_date = finding_filters.get_approval_date(parent)

    finding_vulns_loader: DataLoader = info.context.loaders['finding_vulns']
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)
    vulns = vuln_domain.filter_zero_risk(vulns)

    return finding_domain.get_age_finding(vulns, release_date)
