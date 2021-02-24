# Standard
from typing import cast

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.domain import user as user_domain
from backend.typing import Me


async def resolve(
    parent: Me,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> bool:
    user_email: str = cast(str, parent['user_email'])
    is_concurrent_cession: bool = bool(
        await user_domain.get_data(user_email, 'is_concurrent_session')
    )

    return is_concurrent_cession
