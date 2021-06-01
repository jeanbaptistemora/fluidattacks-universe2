from custom_types import (
    Me,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    cast,
)
from users import (
    domain as users_domain,
)


async def resolve(
    parent: Me, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    user_email: str = cast(str, parent["user_email"])
    remember: bool = bool(
        await users_domain.get_data(user_email, "legal_remember")
    )
    return remember
