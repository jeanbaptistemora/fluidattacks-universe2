from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from db_model.subscriptions.types import (
    Subscription,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Union,
)

NumericType = Union[Decimal, float, int]


def frequency_to_period(*, frequency: str) -> int:
    mapping: dict[str, int] = {
        "HOURLY": 3600,
        "DAILY": 86400,
        "WEEKLY": 604800,
        "MONTHLY": 2419200,
    }
    return mapping[frequency]


def period_to_frequency(*, period: NumericType) -> str:
    mapping: dict[int, str] = {
        3600: "HOURLY",
        86400: "DAILY",
        604800: "WEEKLY",
        2419200: "MONTHLY",
    }
    return mapping[int(period)]


def format_subscription(item: Item) -> Subscription:
    return Subscription(
        email=item["pk"]["email"],
        entity=SubscriptionEntity[item["sk"]["entity"]],
        frequency=SubscriptionFrequency[
            period_to_frequency(period=item["period"])
        ],
        subject=item["sk"]["subject"],
    )
