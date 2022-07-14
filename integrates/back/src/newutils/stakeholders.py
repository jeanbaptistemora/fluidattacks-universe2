from db_model.enums import (
    Notification,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    Stakeholder,
    StakeholderAccessToken,
    StakeholderMetadataToUpdate,
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
    Union,
)


def format_access_token(item: Item) -> StakeholderAccessToken:
    return StakeholderAccessToken(
        iat=int(item["iat"]),
        jti=item["jti"],
        salt=item["salt"],
    )


def format_metadata_item(metadata: StakeholderMetadataToUpdate) -> Item:
    item = {
        "first_name": metadata.first_name,
        "last_name": metadata.last_name,
        "is_concurrent_session": metadata.is_concurrent_session,
        "push_tokens": metadata.push_tokens,
        "registered": metadata.is_registered,
        "access_token": {
            "iat": metadata.access_token.iat,
            "jti": metadata.access_token.jti,
            "salt": metadata.access_token.salt,
        }
        if metadata.access_token
        else None,
        "legal_remember": metadata.legal_remember,
        "registration_date": datetime_utils.convert_from_iso_str(
            metadata.registration_date
        )
        if metadata.registration_date
        else None,
        "last_login": datetime_utils.convert_from_iso_str(
            metadata.last_login_date
        )
        if metadata.last_login_date
        else None,
        "tours": {
            "new_group": metadata.tours.new_group,
            "new_root": metadata.tours.new_root,
        }
        if metadata.tours
        else None,
        "phone": {
            "calling_country_code": metadata.phone.calling_country_code,
            "country_code": metadata.phone.country_code,
            "national_number": metadata.phone.national_number,
        }
        if metadata.phone
        else None,
    }
    if (
        metadata.access_token
        and metadata.access_token.iat == 0
        and metadata.access_token.jti == ""
    ):
        item["access_token"] = []
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }


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


def format_phone(item: Union[Item, tuple]) -> StakeholderPhone:
    if isinstance(item, dict):
        return StakeholderPhone(
            calling_country_code=item["calling_country_code"],
            country_code=item["country_code"],
            national_number=item["national_number"],
        )
    return StakeholderPhone(
        calling_country_code=item[0],
        country_code=item[1],
        national_number=item[2],
    )


def format_tours(item: Item) -> StakeholderTours:
    return StakeholderTours(
        new_group=bool(item["new_group"]),
        new_root=bool(item["new_root"]),
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
        responsibility=item_legacy.get("responsibility", None),
    )


def format_invitation_state(invitation: Item, is_registered: bool) -> str:
    if invitation and not invitation["is_used"]:
        return "PENDING"
    if not is_registered:
        return "UNREGISTERED"
    return "CONFIRMED"


def format_stakeholder_item(stakeholder: Stakeholder) -> Item:
    item = {
        "email": stakeholder.email,
        "first_name": stakeholder.first_name,
        "last_name": stakeholder.last_name,
        "access_token": {
            "iat": stakeholder.access_token.iat,
            "jti": stakeholder.access_token.jti,
            "salt": stakeholder.access_token.salt,
        }
        if stakeholder.access_token
        else None,
        "is_concurrent_session": stakeholder.is_concurrent_session,
        "date_joined": datetime_utils.convert_from_iso_str(
            stakeholder.registration_date
        )
        if stakeholder.registration_date
        else None,
        "last_login": datetime_utils.convert_from_iso_str(
            stakeholder.last_login_date
        )
        if stakeholder.last_login_date
        else None,
        "legal_remember": stakeholder.legal_remember,
        "phone": stakeholder.phone,
        "push_tokens": stakeholder.push_tokens,
        "registered": stakeholder.is_registered,
        "tours": {
            "new_group": stakeholder.tours.new_group,
            "new_root": stakeholder.tours.new_root,
        },
        "responsibility": stakeholder.responsibility,
    }
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }
