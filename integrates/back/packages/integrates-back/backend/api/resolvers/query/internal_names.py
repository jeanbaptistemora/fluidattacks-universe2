# Standard
# None

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login
)
from backend.typing import InternalName
from names import domain as names_domain


@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async
)
async def resolve(
    _parent: None,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> InternalName:
    entity: str = kwargs['entity']

    return {'name': await names_domain.get_name(entity.lower())}
