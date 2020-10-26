# Standard
from typing import cast, Dict, List, Optional

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
    **kwargs: str
) -> List[Vulnerability]:
    finding_id: str = cast(Dict[str, str], parent)['id']

    state: Optional[str] = kwargs.get('state')

    finding_vulns_loader: DataLoader = info.context.loaders['finding_vulns']
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)

    if state:
        return [
            vuln
            for vuln in vulns
            if (vuln['current_state'] == state and
                (vuln['current_approval_status'] != 'PENDING' or
                 vuln['last_approved_status']))
        ]

    return vulns
