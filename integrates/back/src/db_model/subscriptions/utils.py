# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from db_model.subscriptions.types import (
    Subscription,
)
from dynamodb.types import (
    Item,
)


def format_subscription_item(subscription: Subscription) -> Item:
    return {
        "email": subscription.email,
        "entity": subscription.entity,
        "frequency": subscription.frequency,
        "subject": subscription.subject,
        "state": {"modified_date": subscription.modified_date},
    }


def format_subscriptions(item: Item) -> Subscription:
    return Subscription(
        email=item["email"],
        entity=SubscriptionEntity[item["entity"]],
        frequency=SubscriptionFrequency[item["frequency"]],
        subject=item["subject"],
        modified_date=item.get("state", {}).get("modified_date"),
    )
