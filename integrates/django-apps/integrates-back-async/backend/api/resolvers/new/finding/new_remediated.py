# Standard
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
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

    open_vulns: List[Vulnerability] = [
        vuln
        for vuln in vulns
        if vuln['last_approved_status'] == 'open'
    ]
    remediated_vulns: List[Vulnerability] = [
        vuln
        for vuln in vulns if vuln['remediated']
    ]

    return len(remediated_vulns) == len(open_vulns)
