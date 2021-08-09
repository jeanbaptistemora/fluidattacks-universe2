from custom_types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    cast,
    Dict,
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> int:
    response: int = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding",
        attr="open_vulnerabilities",
        id=cast(Dict[str, str], parent)["id"],
    )
    return response


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> int:
    finding_id: str = cast(Dict[str, str], parent)["id"]
    open_vulnerabilities = await findings_domain.get_open_vulnerabilities(
        info.context.loaders, finding_id
    )
    return open_vulnerabilities
