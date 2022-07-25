from db_model.organization_access.constants import (
    ORGANIZATION_ID_PREFIX,
    STAKEHOLDER_PREFIX,
)
from db_model.organization_access.enums import (
    InvitiationState,
)
from db_model.organization_access.types import (
    OrganizationAccess,
    OrganizationAccessMetadataToUpdate,
    OrganizationInvitation,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Optional,
)


def remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def remove_stakeholder_prefix(email: str) -> str:
    return email.lstrip(STAKEHOLDER_PREFIX)


def format_org_invitation_state(
    invitation: Optional[OrganizationInvitation], is_registered: bool
) -> str:
    if invitation and not invitation.is_used:
        return InvitiationState.PENDING
    if not is_registered:
        return InvitiationState.UNREGISTERED
    return InvitiationState.REGISTERED


def format_invitation(invitation: Item) -> OrganizationInvitation:
    return OrganizationInvitation(
        is_used=bool(invitation["is_used"]),
        role=invitation["role"],
        url_token=invitation["url_token"],
    )


def format_organization_access(item: Item) -> OrganizationAccess:
    return OrganizationAccess(
        organization_id=item["pk"],
        email=remove_stakeholder_prefix(item["sk"]),
        has_access=bool(item["has_access"])
        if item.get("has_access") is not None
        else None,
        invitation=format_invitation(item["invitation"])
        if item.get("invitation")
        else None,
        expiration_time=int(item["expiration_time"])
        if item.get("expiration_time")
        else None,
    )


def format_metadata_item(
    metadata: OrganizationAccessMetadataToUpdate,
) -> Item:
    item: Item = {
        "has_access": metadata.has_access,
        "invitation": {
            "is_used": metadata.invitation.is_used,
            "role": metadata.invitation.role,
            "url_token": metadata.invitation.url_token,
        }
        if metadata.invitation
        else None,
        "expiration_time": metadata.expiration_time,
    }
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }
