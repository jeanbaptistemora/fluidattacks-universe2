import authz
from custom_types import (
    Me,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    cast,
)


async def resolve(
    parent: Me, _info: GraphQLResolveInfo, **_kwargs: str
) -> str:
    user_email: str = cast(str, parent["user_email"])
    return await authz.get_user_level_role(user_email)
