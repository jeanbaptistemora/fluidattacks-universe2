from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from typing import (
    NamedTuple,
)


class Subscription(NamedTuple):
    email: str
    entity: SubscriptionEntity
    frequency: SubscriptionFrequency
    subject: str
