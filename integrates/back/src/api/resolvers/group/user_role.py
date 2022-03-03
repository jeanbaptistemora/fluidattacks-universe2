import authz
from db_model.groups.types import (
    Group,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from typing import (
    Any,
    Dict,
    Union,
)


async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    return await authz.get_group_level_role(user_email, group_name)
