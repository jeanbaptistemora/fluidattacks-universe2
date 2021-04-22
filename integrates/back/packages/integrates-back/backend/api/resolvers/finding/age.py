# Standard
from functools import partial
from typing import (
    cast,
    Dict,
)

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import Finding
from findings import domain as findings_domain
from redis_cluster.operations import redis_get_or_set_entity_attr


async def resolve(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int:
    response: int = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **_kwargs),
        entity='finding',
        attr='age',
        id=cast(str, parent['id']),
    )

    return response


async def resolve_no_cache(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> int:
    finding_id: str = cast(str, parent['id'])
    age = cast(
        int,
        await findings_domain.get_finding_age(info.context.loaders, finding_id)
    )

    return age
