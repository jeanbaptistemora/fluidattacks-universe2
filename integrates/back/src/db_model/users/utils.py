from .types import (
    NotificationsPreferences,
    User,
)
from dynamodb.types import (
    Item,
)


def format_user(item: Item) -> User:

    return User(
        email=item["pk"].split("#")[1],
        notifications_preferences=NotificationsPreferences(
            email=item["notifications_preferences"]["email"]
        ),
    )
