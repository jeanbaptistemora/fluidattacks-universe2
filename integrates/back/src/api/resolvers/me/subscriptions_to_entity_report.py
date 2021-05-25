from typing import (
    Dict,
    List,
    cast,
)

from graphql.type.definition import GraphQLResolveInfo

from custom_types import Me
from subscriptions import domain as subscriptions_domain


async def resolve(
    parent: Me, _info: GraphQLResolveInfo, **_kwargs: None
) -> List[Dict[str, str]]:
    user_email: str = cast(str, parent["user_email"])

    return cast(
        List[Dict[str, str]],
        await subscriptions_domain.get_user_subscriptions_to_entity_report(
            user_email=user_email
        ),
    )
