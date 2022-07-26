from db_model.organization_access.enums import (
    InvitiationState,
)
from db_model.organization_access.types import (
    OrganizationInvitation,
)
from typing import (
    Optional,
)


def format_org_invitation_state(
    invitation: Optional[OrganizationInvitation], is_registered: bool
) -> str:
    if invitation and not invitation.is_used:
        return InvitiationState.PENDING
    if not is_registered:
        return InvitiationState.UNREGISTERED
    return InvitiationState.REGISTERED
