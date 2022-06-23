from ..enums import (
    Notification,
)
from .types import (
    NotificationsPreferences,
    Stakeholder,
    StakeholderAccessToken,
    StakeholderPhone,
    StakeholderTours,
)
from dynamodb.types import (
    Item,
)


def format_access_token(item: Item) -> StakeholderAccessToken:
    return StakeholderAccessToken(
        iat=int(item["iat"]),
        jti=item["jti"],
        salt=item["salt"],
    )


def format_phone(item: Item) -> StakeholderPhone:
    return StakeholderPhone(
        calling_country_code=item["calling_country_code"],
        country_code=item["country_code"],
        national_number=item["national_number"],
    )


def format_tours(item: Item) -> StakeholderTours:
    return StakeholderTours(
        new_group=bool(item["new_group"]),
        new_root=bool(item["new_root"]),
    )


def format_stakeholder(item: Item) -> Stakeholder:
    preferences: list[str] = []
    if item.get("notifications_preferences"):
        preferences = [
            item
            for item in item["notifications_preferences"]["email"]
            if item in Notification.__members__
        ]
    return Stakeholder(
        access_token=format_access_token(item["access_token"])
        if item.get("access_token")
        else None,
        email=item["email"],
        first_name=item.get("first_name", ""),
        is_concurrent_session=item.get("is_concurrent_session", False),
        is_registered=item.get("is_registered", False),
        last_login_date=item.get("last_login"),
        last_name=item.get("last_name", ""),
        legal_remember=item.get("legal_remember", False),
        notifications_preferences=NotificationsPreferences(email=preferences),
        phone=format_phone(item["phone"]) if item.get("phone") else None,
        push_tokens=item.get("push_tokens"),
        registration_date=item.get("date_joined"),
        tours=format_tours(item["tours"])
        if item.get("tours")
        else StakeholderTours(),
    )
