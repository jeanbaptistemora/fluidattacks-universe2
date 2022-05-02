from graphql.type.definition import (
    GraphQLResolveInfo,
)
from subscriptions import (
    domain as subscriptions_domain,
)
from typing import (
    Any,
    Dict,
    List,
)


async def resolve(
    parent: Dict[str, Any], _info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[str, str]]:
    user_email = str(parent["user_email"])

    return await subscriptions_domain.get_user_subscriptions_to_entity_report(
        user_email=user_email
    )
