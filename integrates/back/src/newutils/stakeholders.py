from db_model.enums import (
    Notification,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    Stakeholder,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Optional,
)


def format_stakeholder(
    item_legacy: Item, item_vms: Optional[Item]
) -> Stakeholder:
    preferences: list[str] = []
    if item_vms and item_vms.get("notifications_preferences"):
        preferences = [
            item
            for item in item_vms["notifications_preferences"]["email"]
            if item in Notification.__members__
        ]
    return Stakeholder(
        email=item_legacy["email"],
        notifications_preferences=NotificationsPreferences(email=preferences),
    )
