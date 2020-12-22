# Standard
from typing import cast, Dict, List

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import get_entity_cache_async
from backend.domain import finding as finding_domain
from backend.filters import finding as finding_filters
from backend.typing import (
    Tracking as TrackingItem,
    Finding
)


@get_entity_cache_async
async def resolve(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[TrackingItem]:
    finding_id: str = cast(str, parent['id'])
    is_finding_released = finding_filters.is_released(parent)

    finding_vulns_loader: DataLoader = info.context.loaders['finding_vulns']

    if is_finding_released:
        vulns = await finding_vulns_loader.load(finding_id)

        return finding_domain.get_tracking_vulnerabilities_new(vulns)

    return []
