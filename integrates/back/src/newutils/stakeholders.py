from db_model.enums import (
    Notification,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    Stakeholder,
    StakeholderAccessToken,
    StakeholderPhone,
    StakeholderTours,
)
from dynamodb.types import (
    Item,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Optional,
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


def format_notifications_preferences(
    item_vms: Optional[Item],
) -> NotificationsPreferences:
    email_preferences: list[str] = []
    sms_preferences: list[str] = []
    if item_vms and item_vms.get("notifications_preferences"):
        email_preferences = [
            item
            for item in item_vms["notifications_preferences"]["email"]
            if item in Notification.__members__
        ]
        if "sms" in item_vms["notifications_preferences"]:
            sms_preferences = [
                item
                for item in item_vms["notifications_preferences"]["sms"]
                if item in Notification.__members__
            ]
    return NotificationsPreferences(
        email=email_preferences,
        sms=sms_preferences,
    )


def format_stakeholder(
    item_legacy: Item, item_vms: Optional[Item]
) -> Stakeholder:
    return Stakeholder(
        access_token=format_access_token(item_legacy["access_token"])
        if item_legacy.get("access_token")
        else None,
        email=item_legacy["email"],
        first_name=item_legacy.get("first_name", ""),
        is_concurrent_session=item_legacy.get("is_concurrent_session", False),
        is_registered=item_legacy.get("registered", False),
        last_login_date=datetime_utils.convert_to_iso_str(
            item_legacy["last_login"]
        )
        if item_legacy.get("last_login")
        else None,
        last_name=item_legacy.get("last_name", ""),
        legal_remember=item_legacy.get("legal_remember", False),
        notifications_preferences=format_notifications_preferences(item_vms),
        phone=format_phone(item_legacy["phone"])
        if item_legacy.get("phone")
        else None,
        push_tokens=item_legacy.get("push_tokens"),
        registration_date=datetime_utils.convert_to_iso_str(
            item_legacy["date_joined"]
        )
        if item_legacy.get("date_joined")
        else None,
        tours=format_tours(item_legacy["tours"])
        if item_legacy.get("tours")
        else StakeholderTours(),
    )
