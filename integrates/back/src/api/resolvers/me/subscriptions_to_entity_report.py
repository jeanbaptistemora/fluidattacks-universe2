from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    subscriptions as subscriptions_utils,
)
from subscriptions import (
    domain as subscriptions_domain,
)
from typing import (
    Any,
)


async def _format_subscriptions(
    subscriptions: list[dict[str, Any]],
) -> list[dict[str, str]]:
    return [
        {
            "entity": subscription["sk"]["entity"],
            "frequency": subscriptions_utils.period_to_frequency(
                period=subscription["period"]
            ),
            "subject": subscription["sk"]["subject"],
        }
        for subscription in subscriptions
        if subscription["sk"]["meta"] == "entity_report"
    ]


async def resolve(
    parent: dict[str, Any],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[dict[str, str]]:
    email = str(parent["user_email"])
    subscriptions = await subscriptions_domain.get_user_subscriptions(email)

    return await _format_subscriptions(subscriptions)
