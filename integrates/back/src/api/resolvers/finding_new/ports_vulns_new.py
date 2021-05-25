from functools import partial
from typing import List

from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

from custom_types import Vulnerability
from db_model.findings.types import Finding
from redis_cluster.operations import redis_get_or_set_entity_attr


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Vulnerability]:
    response: List[Vulnerability] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding_new",
        attr="ports_vulns_new",
        group=parent.group_name,
        id=parent.id,
    )
    return response


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Vulnerability]:
    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns
    vulns: List[Vulnerability] = await finding_vulns_loader.load(parent.id)
    return [vuln for vuln in vulns if vuln["vuln_type"] == "ports"]
