# Standard
from functools import partial
from typing import (
    cast,
    Dict,
    List,
)

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import (
    Finding,
    Vulnerability,
)
from redis_cluster.operations import redis_get_or_set_entity_attr
from vulnerabilities import domain as vulns_domain


async def resolve(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> int:
    response: int = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='finding',
        attr='state',
        id=cast(str, parent['id']),
    )

    return response


async def resolve_no_cache(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    finding_id: str = cast(Dict[str, str], parent)['id']

    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)
    vulns = vulns_domain.filter_non_confirmed_zero_risk_vuln(vulns)
    open_vulns = vulns_domain.filter_open_vulnerabilities(vulns)

    return 'open' if open_vulns else 'closed'
