# Standard
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
from backend.domain import vulnerability as vuln_domain
from backend.typing import Finding, Vulnerability


@get_entity_cache_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> bool:
    finding_id: str = cast(Dict[str, str], parent)['id']

    finding_vulns_loader: DataLoader = info.context.loaders['finding_vulns']
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)

    vulns = vuln_domain.filter_zero_risk(vulns)
    open_vulns = vuln_domain.filter_open_vulnerabilities(vulns)
    remediated_vulns = vuln_domain.filter_remediated(vulns)

    return len(remediated_vulns) == len(open_vulns)
