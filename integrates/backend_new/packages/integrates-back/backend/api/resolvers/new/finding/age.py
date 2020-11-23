# Standard
from datetime import datetime
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


@get_entity_cache_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> int:
    finding_id: str = cast(Dict[str, str], parent)['id']
    release_date: datetime = cast(Dict[str, datetime], parent)['release_date']

    finding_vulns_loader: DataLoader = info.context.loaders['finding_vulns']
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)
    vulns = vuln_domain.filter_zero_risk(vulns)

    return finding_domain.get_age_finding(vulns, cast(str, release_date))
