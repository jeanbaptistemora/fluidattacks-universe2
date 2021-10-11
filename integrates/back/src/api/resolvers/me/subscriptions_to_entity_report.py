from custom_types import (
    Me,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from subscriptions import (
    domain as subscriptions_domain,
)
from typing import (
    cast,
    Dict,
    List,
)


async def resolve(
    parent: Me, _info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[str, str]]:
    user_email: str = parent["user_email"]

    return cast(
        List[Dict[str, str]],
        await subscriptions_domain.get_user_subscriptions_to_entity_report(
            user_email=user_email
        ),
    )
