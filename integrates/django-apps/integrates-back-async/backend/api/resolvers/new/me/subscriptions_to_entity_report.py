# Standard
from typing import Dict, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.domain import subscriptions as subscriptions_domain
from backend.typing import Me


async def resolve(
    _parent: Me,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Dict[str, str]]:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    return await subscriptions_domain.get_user_subscriptions_to_entity_report(
        user_email=user_email,
    )
