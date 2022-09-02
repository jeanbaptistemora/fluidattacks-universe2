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
