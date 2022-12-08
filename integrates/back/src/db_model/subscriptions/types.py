from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from typing import (
    NamedTuple,
    Optional,
)


class SubscriptionState(NamedTuple):
    modified_date: Optional[str]


class Subscription(NamedTuple):
    email: str
    entity: SubscriptionEntity
    frequency: SubscriptionFrequency
    subject: str
    state: SubscriptionState
