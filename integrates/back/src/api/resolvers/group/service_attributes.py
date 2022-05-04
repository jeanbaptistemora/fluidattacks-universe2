import authz
from db_model.groups.types import (
    Group,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[str]:
    return sorted(await authz.get_group_service_attributes(parent))
