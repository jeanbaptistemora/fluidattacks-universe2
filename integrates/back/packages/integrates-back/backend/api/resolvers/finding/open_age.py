# Standard
from functools import (
    partial,
)
from typing import cast, Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.dal.helpers.redis import (
    redis_get_or_set_entity_attr,
)
from backend.domain import (
    finding as finding_domain,
)
from backend.typing import Finding


async def resolve(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> int:
    response: int = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='finding',
        attr='open_age',
        id=cast(str, parent['id']),
    )

    return response


async def resolve_no_cache(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> int:
    finding_id: str = cast(str, parent['id'])
    open_age = cast(
        int,
        await finding_domain.get_finding_open_age(
            info.context.loaders,
            finding_id
        )
    )

    return open_age
