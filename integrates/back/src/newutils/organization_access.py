from db_model.organization_access.enums import (
    OrganizationInvitiationState,
)
from db_model.organization_access.types import (
    OrganizationInvitation,
)


def format_invitation_state(
    invitation: OrganizationInvitation | None, is_registered: bool
) -> OrganizationInvitiationState:
    if invitation and not invitation.is_used:
        return OrganizationInvitiationState.PENDING
    if not is_registered:
        return OrganizationInvitiationState.UNREGISTERED
    return OrganizationInvitiationState.REGISTERED
