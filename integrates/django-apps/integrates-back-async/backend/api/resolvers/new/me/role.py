# Standard
from typing import Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import authz, util
from backend.exceptions import InvalidParameter
from backend.typing import Me


async def resolve(
    _parent: Me,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> str:
    user_data: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']

    entity: str = kwargs['entity']
    identifier: str = kwargs.get('identifier', '')

    if entity == 'USER':
        return await authz.get_user_level_role(user_email)

    if entity == 'PROJECT' and identifier:
        return await authz.get_group_level_role(user_email, identifier)

    if entity == 'ORGANIZATION' and identifier:
        return await authz.get_organization_level_role(user_email, identifier)

    raise InvalidParameter()
