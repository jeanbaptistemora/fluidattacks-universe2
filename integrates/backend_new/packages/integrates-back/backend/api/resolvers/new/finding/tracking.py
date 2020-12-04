# Standard
from typing import cast, Dict, List, Union

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
from backend.domain import finding as finding_domain
from backend.typing import Finding
from backend.filters import finding as finding_filters


@get_entity_cache_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Dict[str, Union[str, int]]]:
    finding_id: str = cast(Dict[str, str], parent)['id']
    is_finding_released = finding_filters.is_released(
        cast(Dict[str, Finding], parent)
    )

    finding_vulns_loader: DataLoader = info.context.loaders['finding_vulns']

    if is_finding_released:
        vulns = await finding_vulns_loader.load(finding_id)

        return await finding_domain.get_tracking_vulnerabilities(vulns)

    return []
