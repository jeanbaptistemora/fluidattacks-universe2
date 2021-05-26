from functools import partial
from typing import List

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from custom_types import Tracking as TrackingItem
from db_model.findings.types import Finding
from findings import domain as findings_domain
from redis_cluster.operations import redis_get_or_set_entity_attr


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[TrackingItem]:
    response: List[TrackingItem] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding_new",
        attr="tracking_new",
        group=parent.group_name,
        id=parent.id,
    )
    return response


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[TrackingItem]:
    tracking = []
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns
    if parent.approval:
        vulns = await finding_vulns_loader.load(parent.id)
        tracking = findings_domain.get_tracking_vulnerabilities(vulns)
    return tracking
