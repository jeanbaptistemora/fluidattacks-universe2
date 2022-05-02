from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Dict,
)
from users import (
    domain as users_domain,
)


async def resolve(
    parent: Dict[str, Any], _info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, bool]:
    user_email = str(parent["user_email"])
    data: dict = await users_domain.get_by_email(user_email)

    return data["tours"]
