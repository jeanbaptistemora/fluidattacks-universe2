# Standard
from functools import partial
from typing import List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from custom_types import Vulnerability
from model.findings.types import Finding
from redis_cluster.operations import redis_get_or_set_entity_attr
from vulnerabilities import domain as vulns_domain


async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> str:
    response: str = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='finding_new',
        attr='state_new',
        group=parent.group_name,
        id=parent.id,
    )
    return response


async def resolve_no_cache(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns
    vulns: List[Vulnerability] = await finding_vulns_loader.load(parent.id)
    vulns = vulns_domain.filter_non_confirmed_zero_risk_vuln(vulns)
    open_vulns = vulns_domain.filter_open_vulnerabilities(vulns)
    return 'open' if open_vulns else 'closed'
