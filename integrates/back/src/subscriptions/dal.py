# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from db_model.subscriptions.enums import (
    SubscriptionFrequency,
)
from db_model.subscriptions.types import (
    Subscription,
)
from decimal import (
    Decimal,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from newutils.encodings import (
    key_to_mapping,
    mapping_to_key,
)
from newutils.subscriptions import (
    format_subscription,
    frequency_to_period,
)
from typing import (
    Any,
    Dict,
    List,
    Union,
)

# Constants
SUBSCRIPTIONS_TABLE = "fi_subscriptions"
NumericType = Union[Decimal, float, int]


def _unpack_items(items: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:
    return [
        {
            **item,
            "pk": key_to_mapping(item["pk"]),
            "sk": key_to_mapping(item["sk"]),
        }
        for item in items
    ]


async def get_all_subscriptions(
    *, frequency: SubscriptionFrequency
) -> tuple[Subscription, ...]:
    frequency_period = frequency_to_period(frequency=frequency)
    results = await dynamodb_ops.query(
        query_attrs=dict(
            FilterExpression=Attr("period").eq(frequency_period),
            IndexName="pk_meta",
            KeyConditionExpression=(
                Key("pk_meta").eq("user") & Key("sk_meta").eq("entity_report")
            ),
        ),
        table=SUBSCRIPTIONS_TABLE,
    )
    subscription_items = _unpack_items(results)
    return tuple(format_subscription(item) for item in subscription_items)


async def _subscribe_user_to_entity_report(
    *,
    event_period: NumericType,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    return await dynamodb_ops.put_item(
        item=dict(
            pk=mapping_to_key(
                {
                    "meta": "user",
                    "email": user_email,
                }
            ),
            sk=mapping_to_key(
                {
                    "meta": "entity_report",
                    "entity": report_entity,
                    "subject": report_subject,
                }
            ),
            period=Decimal(event_period),
            pk_meta="user",
            sk_meta="entity_report",
        ),
        table=SUBSCRIPTIONS_TABLE,
    )


async def add(*, subscription: Subscription) -> None:
    event_period: int = frequency_to_period(
        frequency=subscription.frequency.value
    )
    await _subscribe_user_to_entity_report(
        event_period=event_period,
        report_entity=subscription.entity.value,
        report_subject=subscription.subject,
        user_email=subscription.email,
    )


async def remove(
    *,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> None:
    await dynamodb_ops.delete_item(
        delete_attrs=dynamodb_ops.DynamoDelete(
            Key=dict(
                pk=mapping_to_key(
                    {
                        "meta": "user",
                        "email": user_email,
                    }
                ),
                sk=mapping_to_key(
                    {
                        "meta": "entity_report",
                        "entity": report_entity,
                        "subject": report_subject,
                    }
                ),
            )
        ),
        table=SUBSCRIPTIONS_TABLE,
    )
