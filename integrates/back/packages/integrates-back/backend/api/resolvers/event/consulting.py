# Standard
from functools import (
    partial,
)
from typing import (
    Any,
    cast,
    Dict,
    List,
)

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.typing import Comment, Event
from comments import domain as comments_domain
from redis_cluster.operations import redis_get_or_set_entity_attr


async def resolve_no_cache(
    parent: Event,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> List[Comment]:
    event_id: str = cast(str, parent['id'])
    group_name: str = cast(str, parent['project_name'])

    user_data: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']

    return cast(
        List[Comment],
        await comments_domain.get_event_comments(
            group_name,
            event_id,
            user_email
        )
    )


async def resolve(
    parent: Event,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> List[Comment]:
    response: List[Comment] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='event',
        attr='consulting',
        id=cast(str, parent['id']),
    )

    return response
