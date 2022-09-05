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
    }


def format_subscriptions(item: Item) -> Subscription:
    return Subscription(
        email=item["email"],
        entity=SubscriptionEntity[item["entity"]],
        frequency=SubscriptionFrequency(item["frequency"]),
        subject=item["subject"],
    )
