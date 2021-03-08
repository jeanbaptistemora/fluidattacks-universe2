# Standard
from functools import (
    partial,
)
from typing import cast, Dict, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.dal.helpers.redis import (
    redis_get_or_set_entity_attr,
)
from backend import util
from backend.typing import Comment, Finding
from comments import domain as comments_domain


async def resolve(
    parent: Dict[str, Finding],
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> List[Comment]:
    response: List[Comment] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='finding',
        attr='consulting',
        id=cast(str, parent['id']),
    )

    return response


async def resolve_no_cache(
    parent: Finding,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Comment]:
    finding_id: str = cast(Dict[str, str], parent)['id']
    group_name: str = cast(Dict[str, str], parent)['project_name']

    user_data: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']

    return cast(
        List[Comment],
        await comments_domain.get_comments(
            group_name,
            finding_id,
            user_email,
            info
        )
    )
