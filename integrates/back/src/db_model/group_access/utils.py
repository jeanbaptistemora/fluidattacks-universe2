from .types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
    GroupConfirmDeletion,
    GroupInvitation,
)
from dynamodb.types import (
    Item,
)


def format_group_access(item: Item) -> GroupAccess:
    return GroupAccess(
        email=item["email"],
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
            "responsibility": metadata.responsibility,
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
