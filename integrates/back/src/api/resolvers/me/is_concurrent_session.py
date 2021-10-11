from custom_types import (
    Me,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from users import (
    domain as users_domain,
)


async def resolve(
    parent: Me, _info: GraphQLResolveInfo, **_kwargs: None
) -> bool:
    user_email: str = parent["user_email"]
    is_concurrent_session: bool = bool(
        await users_domain.get_data(user_email, "is_concurrent_session")
    )
    return is_concurrent_session
