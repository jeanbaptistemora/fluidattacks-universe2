from .schema import (
    GROUP,
)
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


@GROUP.field("serviceAttributes")
@enforce_group_level_auth_async
def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[str]:
    return sorted(authz.get_group_service_attributes(parent))
