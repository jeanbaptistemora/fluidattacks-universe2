# Standard
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    enforce_group_level_auth_async,
    get_entity_cache_async
)
from backend.typing import Finding, Vulnerability


@enforce_group_level_auth_async
@get_entity_cache_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Vulnerability]:
    finding_id: str = cast(Dict[str, str], parent)['id']

    finding_vulns_loader: DataLoader = info.context.loaders['vulnerability']
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)

    return [
        vuln
        for vuln in vulns
        if vuln['current_approval_status'] == 'PENDING'
    ]
