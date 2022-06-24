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
import simplejson as json  # type: ignore
from typing import (
    Optional,
)


def format_access_token(item: Item) -> StakeholderAccessToken:
    return StakeholderAccessToken(
        iat=int(item["iat"]),
        jti=item["jti"],
        salt=item["salt"],
    )


def format_notifications_preferences(
    item: Optional[Item],
) -> NotificationsPreferences:
    if not item:
        return NotificationsPreferences(
            email=[],
            sms=[],
        )
    email_preferences: list[str] = []
    sms_preferences: list[str] = []
    if "email" in item:
        email_preferences = [
            item for item in item["email"] if item in Notification.__members__
        ]
    if "sms" in item:
        sms_preferences = [
            item for item in item["sms"] if item in Notification.__members__
        ]
    return NotificationsPreferences(
        email=email_preferences,
        sms=sms_preferences,
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
    return Stakeholder(
        access_token=format_access_token(item["access_token"])
        if item.get("access_token")
        else None,
        email=item["email"],
        first_name=item.get("first_name", ""),
        is_concurrent_session=item.get("is_concurrent_session", False),
        is_registered=item.get("is_registered", False),
        last_login_date=item.get("last_login_date"),
        last_name=item.get("last_name", ""),
        legal_remember=item.get("legal_remember", False),
        notifications_preferences=format_notifications_preferences(
            item.get("notifications_preferences")
        ),
        phone=format_phone(item["phone"]) if item.get("phone") else None,
        push_tokens=item.get("push_tokens"),
        registration_date=item.get("registration_date"),
        tours=format_tours(item["tours"])
        if item.get("tours")
        else StakeholderTours(),
    )


def format_stakeholder_item(stakeholder: Stakeholder) -> Item:
    item: Item = json.loads(json.dumps(stakeholder))
    item.pop("responsability", None)
    item.pop("role", None)

    return item
