# Standard
from typing import Dict

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.domain import user as user_domain
from backend.typing import Me


async def resolve(
    _parent: Me,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> bool:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']
    remember: bool = bool(
        await user_domain.get_data(user_email, 'legal_remember')
    )

    return remember
