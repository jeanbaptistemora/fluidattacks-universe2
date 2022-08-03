from db_model.findings.types import (
    Finding,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_squad,
)
from finding_comments import (
    domain as comments_domain,
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
    Dict,
    List,
    Tuple,
)


@concurrent_decorators(
    enforce_group_level_auth_async, require_asm, require_squad
)
async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Dict[str, Any]]:
    response: List[Dict[str, Any]] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="finding",
        attr="consulting",
        id=parent.id,
    )
    return response


async def resolve_no_cache(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[Dict[str, Any], ...]:
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    return await comments_domain.get_comments(
        loaders=info.context.loaders,
        group_name=parent.group_name,
        finding_id=parent.id,
        user_email=user_email,
    )
