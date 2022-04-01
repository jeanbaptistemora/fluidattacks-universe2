from custom_types import (
    Comment,
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
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    Any,
    Dict,
    List,
    Union,
)


@concurrent_decorators(
    enforce_group_level_auth_async, require_asm, require_squad
)
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> List[Comment]:
    response: List[Comment] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="consulting",
        name=parent["name"] if isinstance(parent, dict) else parent.name,
    )
    return response


async def resolve_no_cache(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> List[Comment]:
    group_name: str = str(
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    user_data: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]

    return await group_comments_domain.list_comments(group_name, user_email)
