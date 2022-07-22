from .constants import (
    ORGANIZATION_ID_PREFIX,
    STAKEHOLDER_PREFIX,
)
from .types import (
    OrganizationAccess,
    OrganizationAccessMetadataToUpdate,
    OrganizationInvitation,
)
from dynamodb.types import (
    Item,
)


def add_org_id_prefix(organization_id: str) -> str:
    no_prefix_id = remove_org_id_prefix(organization_id)
    return f"{ORGANIZATION_ID_PREFIX}{no_prefix_id}"


def remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def remove_stakeholder_prefix(email: str) -> str:
    return email.lstrip(STAKEHOLDER_PREFIX)


def format_organization_access(item: Item) -> OrganizationAccess:
    return OrganizationAccess(
        email=item["email"],
        organization_id=add_org_id_prefix(item["organization_id"]),
        expiration_time=int(item["expiration_time"])
        if item.get("expiration_time")
        else None,
        has_access=bool(item["has_access"])
        if item.get("has_access") is not None
        else None,
        invitation=OrganizationInvitation(
            is_used=bool(item["invitation"]["is_used"]),
            role=item["invitation"]["role"],
            url_token=item["invitation"]["url_token"],
        )
        if item.get("invitation")
        else None,
    )


def format_metadata_item(
    metadata: OrganizationAccessMetadataToUpdate,
) -> Item:
    item: Item = {
        "expiration_time": metadata.expiration_time,
        "has_access": metadata.has_access,
        "invitation": {
            "is_used": metadata.invitation.is_used,
            "role": metadata.invitation.role,
            "url_token": metadata.invitation.url_token,
        }
        if metadata.invitation
        else None,
    }
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }
