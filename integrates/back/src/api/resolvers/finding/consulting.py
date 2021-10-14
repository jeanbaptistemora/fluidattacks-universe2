from comments import (
    domain as comments_domain,
)
from custom_types import (
    Comment,
)
from db_model.findings.types import (
    Finding,
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
from newutils import (
    token as token_utils,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    List,
)


@concurrent_decorators(
    enforce_group_level_auth_async, require_asm, require_squad
)
async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Comment]:
    response: List[Comment] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding",
        attr="consulting",
        id=parent.id,
    )
    return response


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Comment]:
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    return await comments_domain.get_comments(
        parent.group_name, parent.id, user_email, info
    )
