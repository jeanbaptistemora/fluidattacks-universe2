from db_model.group_access.enums import (
    GroupInvitiationState,
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
) -> GroupInvitiationState:
    if invitation and not invitation.is_used:
        return GroupInvitiationState.PENDING
    if not is_registered:
        return GroupInvitiationState.UNREGISTERED
    return GroupInvitiationState.REGISTERED


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
        confirm_deletion=GroupConfirmDeletion(
            is_used=bool(item["confirm_deletion"]["is_used"]),
            url_token=item["confirm_deletion"]["url_token"],
        )
        if item.get("confirm_deletion")
        else None,
        email=item["user_email"],
        expiration_time=int(item["expiration_time"])
        if item.get("expiration_time")
        else None,
        group_name=item["project_name"],
        has_access=bool(item["has_access"])
        if item.get("has_access") is not None
        else None,
        invitation=format_invitation(item["invitation"])
        if item.get("invitation")
        else None,
        responsibility=item.get("responsibility"),
    )


def format_group_access_item(
    group_access: GroupAccess,
) -> Item:
    return {
        "confirm_deletion": {
            "is_used": group_access.confirm_deletion.is_used,
            "url_token": group_access.confirm_deletion.url_token,
        }
        if group_access.confirm_deletion
        else None,
        "expiration_time": group_access.expiration_time,
        "has_access": group_access.has_access,
        "invitation": {
            "is_used": group_access.invitation.is_used,
            "role": group_access.invitation.role,
            "url_token": group_access.invitation.url_token,
            "responsibility": group_access.invitation.responsibility,
        }
        if group_access.invitation
        else None,
        "project_name": group_access.group_name,
        "responsibility": group_access.responsibility,
        "user_email": group_access.email,
    }


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
