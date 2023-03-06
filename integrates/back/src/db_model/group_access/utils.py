from .types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
    GroupAccessState,
    GroupConfirmDeletion,
    GroupInvitation,
)
from datetime import (
    datetime,
)
from db_model.utils import (
    get_as_utc_iso_format,
)
from dynamodb.types import (
    Item,
)


def format_group_access(item: Item) -> GroupAccess:
    return GroupAccess(
        email=str(item["email"]).lower().strip(),
        group_name=item["group_name"],
        confirm_deletion=GroupConfirmDeletion(
            is_used=bool(item["confirm_deletion"]["is_used"]),
            url_token=item["confirm_deletion"]["url_token"],
        )
        if item.get("confirm_deletion")
        else None,
        expiration_time=int(item["expiration_time"])
        if item.get("expiration_time")
        else None,
        has_access=bool(item["has_access"])
        if item.get("has_access") is not None
        else None,
        invitation=GroupInvitation(
            is_used=bool(item["invitation"]["is_used"]),
            responsibility=item["invitation"].get("responsibility"),
            role=item["invitation"]["role"],
            url_token=item["invitation"]["url_token"],
        )
        if item.get("invitation")
        else None,
        responsibility=item.get("responsibility"),
        role=item.get("role"),
        state=GroupAccessState(
            modified_date=datetime.fromisoformat(
                item["state"]["modified_date"]
            )
            if item.get("state", {}).get("modified_date")
            else None
        ),
    )


def format_metadata_item(
    email: str,
    group_name: str,
    metadata: GroupAccessMetadataToUpdate,
) -> Item:
    item: Item = {
        "confirm_deletion": {
            "is_used": metadata.confirm_deletion.is_used,
            "url_token": metadata.confirm_deletion.url_token,
        }
        if metadata.confirm_deletion
        else None,
        "email": email.lower().strip(),
        "expiration_time": metadata.expiration_time,
        "group_name": group_name,
        "has_access": metadata.has_access,
        "invitation": {
            "is_used": metadata.invitation.is_used,
            "role": metadata.invitation.role,
            "url_token": metadata.invitation.url_token,
            "responsibility": metadata.responsibility,
        }
        if metadata.invitation
        else None,
        "responsibility": metadata.responsibility,
        "role": metadata.role,
        "state": {
            "modified_date": get_as_utc_iso_format(
                metadata.state.modified_date
            )
        }
        if metadata.state.modified_date
        else None,
    }
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }


def merge_group_access_changes(
    old_access: GroupAccess, changes: GroupAccessMetadataToUpdate
) -> GroupAccessMetadataToUpdate:
    return GroupAccessMetadataToUpdate(
        state=changes.state,
        confirm_deletion=changes.confirm_deletion
        if changes.confirm_deletion
        else old_access.confirm_deletion,
        expiration_time=changes.expiration_time
        if changes.expiration_time
        else old_access.expiration_time,
        has_access=changes.has_access
        if changes.has_access
        else old_access.has_access,
        invitation=changes.invitation
        if changes.invitation
        else old_access.invitation,
        responsibility=changes.responsibility
        if changes.responsibility
        else old_access.responsibility,
        role=changes.role if changes.role else old_access.role,
    )
