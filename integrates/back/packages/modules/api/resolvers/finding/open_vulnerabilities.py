from functools import partial
from typing import (
    Dict,
    List,
    cast,
)

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from custom_types import (
    Finding,
    Vulnerability,
)
from redis_cluster.operations import redis_get_or_set_entity_attr
from vulnerabilities import domain as vulns_domain


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> int:
    response: int = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding",
        attr="open_vulns",
        id=cast(Dict[str, str], parent)["id"],
    )
    return response


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns
    finding_id: str = cast(Dict[str, str], parent)["id"]

    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)
    vulns = vulns_domain.filter_zero_risk(vulns)
    vulns = vulns_domain.filter_open_vulnerabilities(vulns)
    return len(vulns)
