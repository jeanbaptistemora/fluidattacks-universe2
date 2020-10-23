# Standard
from typing import cast, Dict, List, Union

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
from backend.domain import finding as finding_domain
from backend.typing import Finding


@get_entity_cache_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Dict[str, Union[str, int]]]:
    finding_id: str = cast(Dict[str, str], parent)['id']
    release_date: str = cast(Dict[str, str], parent)['release_date']

    finding_vulns_loader: DataLoader = info.context.loaders['vulnerability']

    if release_date:
        vulns = await finding_vulns_loader.load(finding_id)

        return await finding_domain.get_tracking_vulnerabilities(vulns)

    return []
