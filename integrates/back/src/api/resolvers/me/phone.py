from custom_types import (
    Me,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)
from users import (
    domain as users_domain,
)


async def resolve(
    parent: Me, _info: GraphQLResolveInfo, **_kwargs: None
) -> Optional[str]:
    user_email = str(parent["user_email"])
    user_info: dict = await users_domain.get_by_email(user_email)
    return user_info["phone"]
