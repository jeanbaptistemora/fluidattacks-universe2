# Standard
from typing import (
    Dict,
    cast,
)

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
import authz
from backend import util
from backend.typing import Project as Group


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> str:
    group_name: str = cast(str, parent['name'])

    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    return str(await authz.get_group_level_role(user_email, group_name))
