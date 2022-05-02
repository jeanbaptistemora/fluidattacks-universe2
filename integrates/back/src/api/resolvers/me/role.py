import authz
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
)


async def resolve(
    parent: Dict[str, Any], _info: GraphQLResolveInfo, **_kwargs: str
) -> str:
    user_email = str(parent["user_email"])
    return await authz.get_user_level_role(user_email)
