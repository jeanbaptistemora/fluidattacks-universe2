from .types import (
    NotificationsPreferences,
    Stakeholder,
)
from db_model.enums import (
    Notification,
)
from dynamodb.types import (
    Item,
)


def format_stakeholder(item: Item) -> Stakeholder:
    preferences: list[str] = [
        item
        for item in item["notifications_preferences"]["email"]
        if item in Notification.__members__
    ]
    return Stakeholder(
        email=item["pk"].split("#")[1],
        notifications_preferences=NotificationsPreferences(email=preferences),
    )
