from custom_types import (
    Me,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    List,
)
from users import (
    domain as users_domain,
)


async def resolve(
    parent: Me, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    has_mobile_app: bool = False
    user_email: str = parent["user_email"]
    user_attrs: dict = await users_domain.get_attributes(
        user_email, ["push_tokens"]
    )
    tokens: List[str] = user_attrs.get("push_tokens", [])
    if tokens:
        has_mobile_app = True
    return has_mobile_app
