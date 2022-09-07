# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.subscriptions.types import (
    Subscription,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


async def _format_subscriptions(
    subscriptions: list[Subscription],
) -> list[dict[str, str]]:
    return [
        {
            "entity": subscription.entity,
            "frequency": subscription.frequency,
            "subject": subscription.subject,
        }
        for subscription in subscriptions
    ]


async def resolve(
    parent: dict[str, Any],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[dict[str, str]]:
    email = str(parent["user_email"])
    loaders = info.context.loaders
    subscriptions = await loaders.stakeholder_subscriptions.load(email)

    return await _format_subscriptions(subscriptions)
