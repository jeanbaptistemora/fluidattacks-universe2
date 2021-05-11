
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
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> bool:
    response: bool = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='finding',
        attr='new_remediated',
        id=cast(str, parent['id']),
    )
    return response


async def resolve_no_cache(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> bool:
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns
    finding_id: str = cast(Dict[str, str], parent)['id']

    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)
    vulns = vulns_domain.filter_zero_risk(vulns)
    open_vulns = vulns_domain.filter_open_vulnerabilities(vulns)
    remediated_vulns = vulns_domain.filter_remediated(vulns)
    return len(remediated_vulns) == len(open_vulns)
