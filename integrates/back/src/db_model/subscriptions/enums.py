from enum import (
    Enum,
)


class SubscriptionEntity(str, Enum):
    GROUP: str = "GROUP"
    ORGANIZATION: str = "ORGANIZATION"
    PORTFOLIO: str = "PORTFOLIO"
    COMMENTS: str = "COMMENTS"


class SubscriptionFrequency(str, Enum):
    DAILY: str = "DAILY"
    HOURLY: str = "HOURLY"
    MONTHLY: str = "MONTHLY"
    NEVER: str = "NEVER"
    WEEKLY: str = "WEEKLY"
