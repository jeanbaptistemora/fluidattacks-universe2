# Standard
from functools import (
    partial,
)
from typing import cast, Dict, List

# Third party
from aiodataloader import DataLoader
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.dal.helpers.redis import (
    redis_get_or_set_entity_attr,
)
from backend.typing import Finding, Vulnerability


async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **kwargs: None
) -> List[Vulnerability]:
    response: List[Vulnerability] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='finding',
        attr='ports_vulns',
        id=cast(Dict[str, str], parent)['id'],
    )

    return response


async def resolve_no_cache(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Vulnerability]:
    finding_id: str = cast(Dict[str, str], parent)['id']

    finding_vulns_loader: DataLoader = info.context.loaders.finding_vulns
    vulns: List[Vulnerability] = await finding_vulns_loader.load(finding_id)

    return [
        vuln
        for vuln in vulns
        if vuln['vuln_type'] == 'ports'
    ]
