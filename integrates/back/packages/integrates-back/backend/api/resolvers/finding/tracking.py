# Standard
from functools import partial
from typing import (
    cast,
    Dict,
    List,
)

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import (
    Finding,
    Tracking as TrackingItem,
)
from findings import domain as findings_domain
from newutils import findings as findings_utils
from redis_cluster.operations import redis_get_or_set_entity_attr


async def resolve(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **kwargs: None
) -> List[TrackingItem]:
    response: List[TrackingItem] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='finding',
        attr='tracking',
        id=cast(str, parent['id']),
    )

    return response


async def resolve_no_cache(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[TrackingItem]:
    finding_id: str = cast(str, parent['id'])
    is_finding_released = findings_utils.is_released(parent)

    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns

    if is_finding_released:
        vulns = await finding_vulns_loader.load(finding_id)

        return cast(
            List[TrackingItem],
            findings_domain.get_tracking_vulnerabilities(vulns)
        )

    return []
