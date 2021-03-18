# Standard
from typing import cast

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.typing import Me
from users import domain as users_domain


async def resolve(
    parent: Me,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> bool:
    user_email: str = cast(str, parent['user_email'])
    remember: bool = bool(
        await users_domain.get_data(user_email, 'legal_remember')
    )

    return remember
