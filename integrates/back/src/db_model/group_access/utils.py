from .types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
    GroupInvitation,
)
from dynamodb.types import (
    Item,
)


def format_group_access(item: Item) -> GroupAccess:
    return GroupAccess(
        email=item["email"],
        group_name=item["group_name"],
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
