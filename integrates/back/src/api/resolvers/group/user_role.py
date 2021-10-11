import authz
from custom_types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from typing import (
    Dict,
)


async def resolve(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> str:
    group_name: str = parent["name"]

    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    return str(await authz.get_group_level_role(user_email, group_name))
