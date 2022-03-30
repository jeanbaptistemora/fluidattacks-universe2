from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    List,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _: None,
    __: GraphQLResolveInfo,
) -> List[str]:
    response: List[str] = await redis_get_or_set_entity_attr(
        resolve_no_cache,
        entity="groups",
        attr="forces",
    )
    return response


async def resolve_no_cache() -> List[str]:
    groups = await groups_domain.get_groups_with_forces()
    return groups
