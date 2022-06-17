from comments import (
    domain as comments_domain,
)
from db_model.events.types import (
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
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    Any,
)


async def resolve_no_cache(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[dict[str, Any]]:
    event_id = parent.id
    group_name = parent.group_name

    user_data: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]

    return await comments_domain.get_event_comments(
        group_name, event_id, user_email
    )


async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> list[dict[str, Any]]:
    response = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="event",
        attr="consulting",
        id=parent.id,
    )
    return response
