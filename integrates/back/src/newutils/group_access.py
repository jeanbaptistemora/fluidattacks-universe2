from db_model.group_access.enums import (
    InvitiationState,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
    GroupConfirmDeletion,
    GroupInvitation,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Optional,
)


def format_invitation_state(
    invitation: Optional[GroupInvitation], is_registered: bool
) -> str:
    if invitation and not invitation.is_used:
        return InvitiationState.PENDING
    if not is_registered:
        return InvitiationState.UNREGISTERED
    return InvitiationState.REGISTERED


def format_invitation(invitation: Item) -> GroupInvitation:
    return GroupInvitation(
        is_used=bool(invitation["is_used"]),
        role=invitation["role"],
        url_token=invitation["url_token"],
        responsibility=str(invitation["responsibility"])
        if invitation.get("responsibility") is not None
        else None,
    )


def format_group_access(item: Item) -> GroupAccess:
    return GroupAccess(
        email=item["user_email"],
        group_name=item["project_name"],
        confirm_deletion=GroupConfirmDeletion(
            is_used=bool(item["confirm_deletion"]["is_used"]),
            url_token=item["confirm_deletion"]["url_token"],
        )
        if item.get("confirm_deletion")
        else None,
        has_access=bool(item["has_access"])
        if item.get("has_access") is not None
        else None,
        invitation=format_invitation(item["invitation"])
        if item.get("invitation")
        else None,
        expiration_time=int(item["expiration_time"])
        if item.get("expiration_time")
        else None,
        responsibility=str(item["responsibility"])
        if item.get("responsibility") is not None
        else None,
    )


def format_metadata_item(
    metadata: GroupAccessMetadataToUpdate,
) -> Item:
    item: Item = {
        "confirm_deletion": {
            "is_used": metadata.confirm_deletion.is_used,
            "url_token": metadata.confirm_deletion.url_token,
        }
        if metadata.confirm_deletion
        else None,
        "expiration_time": metadata.expiration_time,
        "has_access": metadata.has_access,
        "invitation": {
            "is_used": metadata.invitation.is_used,
            "role": metadata.invitation.role,
            "url_token": metadata.invitation.url_token,
            "responsibility": metadata.invitation.responsibility,
        }
        if metadata.invitation
        else None,
        "responsibility": metadata.responsibility,
    }
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }
