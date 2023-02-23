from datetime import (
    datetime,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from typing import (
    NamedTuple,
)


class SubscriptionState(NamedTuple):
    modified_date: datetime | None


class Subscription(NamedTuple):
    email: str
    entity: SubscriptionEntity
    frequency: SubscriptionFrequency
    subject: str
    state: SubscriptionState
