from functools import partial
from typing import List, Optional

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from custom_types import Vulnerability
from model.findings.types import Finding
from redis_cluster.operations import redis_get_or_set_entity_attr


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Vulnerability]:
    vulns: List[Vulnerability] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding_new",
        attr="vulnerabilities_new",
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
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns_nzr
    vulns: List[Vulnerability] = await finding_vulns_loader.load(parent.id)
    return vulns
