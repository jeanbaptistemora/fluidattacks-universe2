# Standard
from typing import cast

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import authz
from backend.typing import Me
from custom_exceptions import InvalidParameter


async def resolve(
    parent: Me,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> str:
    user_email: str = cast(str, parent['user_email'])

    entity: str = kwargs['entity']
    identifier: str = kwargs.get('identifier', '')
    role = ''

    if entity == 'USER':
        role = await authz.get_user_level_role(user_email)
    elif entity == 'PROJECT' and identifier:
        role = await authz.get_group_level_role(user_email, identifier)
    elif entity == 'ORGANIZATION' and identifier:
        role = await authz.get_organization_level_role(user_email, identifier)
    else:
        raise InvalidParameter()

    return role
