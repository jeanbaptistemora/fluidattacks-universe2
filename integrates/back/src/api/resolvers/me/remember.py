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
) -> bool:
    user_email = str(parent["user_email"])
    remember: bool = bool(
        await users_domain.get_data(user_email, "legal_remember")
    )
    return remember
