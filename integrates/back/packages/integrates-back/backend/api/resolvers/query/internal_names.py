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
from backend.domain import available_name as available_name_domain
from backend.typing import InternalName


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

    return {'name': await available_name_domain.get_name(entity.lower())}
