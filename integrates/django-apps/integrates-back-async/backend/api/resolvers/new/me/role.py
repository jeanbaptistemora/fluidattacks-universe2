# Standard
from typing import cast

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import authz
from backend.exceptions import InvalidParameter
from backend.typing import Me


async def resolve(
    parent: Me,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> str:
    user_email: str = cast(str, parent['user_email'])

    entity: str = kwargs['entity']
    identifier: str = kwargs.get('identifier', '')

    if entity == 'USER':
        return await authz.get_user_level_role(user_email)

    if entity == 'PROJECT' and identifier:
        return await authz.get_group_level_role(user_email, identifier)

    if entity == 'ORGANIZATION' and identifier:
        return await authz.get_organization_level_role(user_email, identifier)

    raise InvalidParameter()
