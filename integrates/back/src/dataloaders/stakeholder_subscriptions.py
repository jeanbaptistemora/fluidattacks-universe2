# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model.subscriptions.types import (
    Subscription,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from dynamodb.types import (
    Item,
)
from newutils import (
    subscriptions as subscriptions_utils,
)
from newutils.encodings import (
    key_to_mapping,
    mapping_to_key,
)
from typing import (
    Iterable,
)

SUBSCRIPTIONS_TABLE = "fi_subscriptions"


def _unpack_items(items: list[Item]) -> list[Item]:
    return [
        {
            **item,
            "pk": key_to_mapping(item["pk"]),
            "sk": key_to_mapping(item["sk"]),
        }
        for item in items
    ]


async def _get_subscription_items(
    *,
    email: str,
) -> list[Item]:
    results = await dynamodb_ops.query(
        query_attrs=dict(
            KeyConditionExpression=Key("pk").eq(
                mapping_to_key(
                    {
                        "meta": "user",
                        "email": email,
                    }
                )
            ),
        ),
        table=SUBSCRIPTIONS_TABLE,
    )
    return _unpack_items(results)


async def _get_stakeholder_subscriptions(
    email: str,
) -> tuple[Subscription, ...]:
    subscription_items = await _get_subscription_items(email=email)

    return tuple(
        subscriptions_utils.format_subscription(item)
        for item in subscription_items
    )


class StakeholderSubscriptionsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> tuple[tuple[Subscription, ...], ...]:
        return await collect(
            _get_stakeholder_subscriptions(email) for email in emails
        )
