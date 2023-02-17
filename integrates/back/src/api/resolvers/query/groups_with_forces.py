from .schema import (
    QUERY,
)
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
from organizations import (
    domain as orgs_domain,
)


@QUERY.field("groupsWithForces")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _: None,
    info: GraphQLResolveInfo,
) -> tuple[str, ...]:
    # All active groups have 'forces' enabled
    return await orgs_domain.get_all_active_group_names(info.context.loaders)
