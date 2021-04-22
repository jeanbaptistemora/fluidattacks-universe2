# Standard
from typing import (
    List,
    cast,
)

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from groups import domain as groups_domain
from redis_cluster.operations import redis_get_or_set_entity_attr


@convert_kwargs_to_snake_case  # type: ignore
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
        entity='projects',
        attr='forces',
    )

    return response


async def resolve_no_cache() -> List[str]:
    projects = await groups_domain.get_groups_with_forces()
    return cast(List[str], projects)
