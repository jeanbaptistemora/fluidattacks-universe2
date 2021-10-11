from comments import (
    domain as comments_domain,
)
from custom_types import (
    Comment,
    Event,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
)


async def resolve_no_cache(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> List[Comment]:
    event_id: str = parent["id"]
    group_name: str = get_key_or_fallback(parent)

    user_data: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]

    return cast(
        List[Comment],
        await comments_domain.get_event_comments(
            group_name, event_id, user_email
        ),
    )


async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> List[Comment]:
    response: List[Comment] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="event",
        attr="consulting",
        id=parent["id"],
    )
    return response
