from datetime import (
    datetime,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from db_model.subscriptions.types import (
    Subscription,
    SubscriptionState,
)
from db_model.utils import (
    get_as_utc_iso_format,
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
        "state": {
            "modified_date": get_as_utc_iso_format(
                subscription.state.modified_date
            )
            if subscription.state.modified_date
            else None
        },
    }


def format_subscriptions(item: Item) -> Subscription:
    modified_date: str = item.get("state", {}).get("modified_date")
    return Subscription(
        email=item["email"],
        entity=SubscriptionEntity[item["entity"]],
        frequency=SubscriptionFrequency[item["frequency"]],
        subject=item["subject"],
        state=SubscriptionState(
            modified_date=datetime.fromisoformat(modified_date)
            if modified_date
            else None,
        ),
    )
