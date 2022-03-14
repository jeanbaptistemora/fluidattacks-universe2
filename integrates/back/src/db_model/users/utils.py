from .types import (
    NotificationsPreferences,
    User,
)
from db_model.enums import (
    Notification,
)
from dynamodb.types import (
    Item,
)
from typing import (
    List,
)


def format_user(item: Item) -> User:
    preferences: List[str] = [
        item
        for item in item["notifications_preferences"]["email"]
        if item in Notification.__members__
    ]
    return User(
        email=item["pk"].split("#")[1],
        notifications_preferences=NotificationsPreferences(email=preferences),
    )
