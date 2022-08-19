from db_model.group_comments.types import (
    GroupComment,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_squad,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_comments import (
    domain as group_comments_domain,
)
from newutils import (
    token as token_utils,
)
from newutils.group_comments import (
    format_group_consulting_resolve,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    Any,
)


@concurrent_decorators(
    enforce_group_level_auth_async, require_asm, require_squad
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> list[dict[str, Any]]:
    response: list[dict[str, Any]] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="consulting",
        name=parent.name,
    )
    return response


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[dict[str, Any]]:
    group_name: str = parent.name
    user_data: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]
    loaders = info.context.loaders
    group_comments: tuple[
        GroupComment, ...
    ] = await group_comments_domain.get_comments(
        loaders, group_name, user_email
    )

    return [
        format_group_consulting_resolve(comment) for comment in group_comments
    ]
