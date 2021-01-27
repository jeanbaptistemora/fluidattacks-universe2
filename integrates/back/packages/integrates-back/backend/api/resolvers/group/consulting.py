# Standard
from functools import (
    partial,
)
from typing import cast, Dict, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.dal.helpers.redis import (
    redis_get_or_set_entity_attr,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates
)
from backend.domain import project as project_domain
from backend.typing import Comment, Project as Group


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: None
) -> List[Comment]:
    response: List[Comment] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='group',
        attr='consulting',
        name=cast(str, parent['name']),
    )

    return response


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Comment]:
    group_name: str = cast(str, parent['name'])
    user_data: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']

    return cast(
        List[Comment],
        await project_domain.list_comments(group_name, user_email)
    )
