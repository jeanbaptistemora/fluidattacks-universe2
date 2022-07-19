from db_model.organization_access.constants import (
    ORGANIZATION_ID_PREFIX,
    STAKEHOLDER_PREFIX,
)
from db_model.organization_access.enums import (
    InvitiationState,
)
from db_model.organization_access.types import (
    OrganizationAccess,
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


def format_invitation_state(
    invitation: Optional[OrganizationInvitation], is_registered: bool
) -> str:
    if invitation and not invitation.is_used:
        return InvitiationState.PENDING
    if not is_registered:
        return InvitiationState.UNREGISTERED
    return InvitiationState.REGISTERED


def format_invitation(invitation: Item) -> OrganizationInvitation:
    return OrganizationInvitation(
        is_used=invitation["is_used"],
        role=invitation["role"],
        url_token=invitation["url_token"],
    )


def format_organization_access(item: Item) -> OrganizationAccess:
    return OrganizationAccess(
        organization_id=remove_org_id_prefix(item["pk"]),
        email=remove_stakeholder_prefix(item["sk"]),
        has_access=item.get("has_access", None),
        invitation=format_invitation(item["invitation"])
        if item.get("invitation")
        else None,
        expiration_time=item.get("expiration_time", None),
    )
