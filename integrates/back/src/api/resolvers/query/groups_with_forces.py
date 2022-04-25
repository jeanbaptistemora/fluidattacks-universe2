from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    domain as orgs_domain,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _: None,
    info: GraphQLResolveInfo,
) -> list[str]:
    response: list[str] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, info),
        entity="groups",
        attr="forces",
    )
    return response


async def resolve_no_cache(
    info: GraphQLResolveInfo,
) -> list[str]:
    loaders: Dataloaders = info.context.loaders
    # All active groups have 'forces' enabled
    all_active_groups = await orgs_domain.get_all_active_groups_typed(loaders)
    return [group.name for group in all_active_groups]
