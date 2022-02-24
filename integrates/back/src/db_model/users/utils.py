from .types import (
    User,
)
from dynamodb.types import (
    Item,
)


def format_user(item: Item) -> User:

    return User(notifications_preferences=item["notifications_preferences"])
