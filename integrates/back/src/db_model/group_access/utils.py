from .types import (
    GroupAccess,
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
