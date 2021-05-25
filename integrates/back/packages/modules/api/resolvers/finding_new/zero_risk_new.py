from functools import partial
from typing import List, Optional

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from custom_types import Vulnerability
from decorators import enforce_group_level_auth_async
from model.findings.types import Finding
from redis_cluster.operations import redis_get_or_set_entity_attr


@enforce_group_level_auth_async
async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Vulnerability]:
    vulns: List[Vulnerability] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding_new",
        attr="zero_risk_new",
        group=parent.group_name,
        id=parent.id,
    )
    state: Optional[str] = kwargs.get("state")
    if state:
        vulns = [
            vulnerability
            for vulnerability in vulns
            if vulnerability["current_state"] == state
        ]
    return vulns


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Vulnerability]:
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns_zr
    zero_risk: List[Vulnerability] = await finding_vulns_loader.load(parent.id)
    return zero_risk
