from db_model.group_access.enums import (
    GroupInvitiationState,
)
from db_model.group_access.types import (
    GroupInvitation,
)


def format_invitation_state(
    invitation: GroupInvitation | None, is_registered: bool
) -> GroupInvitiationState:
    if invitation and not invitation.is_used:
        return GroupInvitiationState.PENDING
    if not is_registered:
        return GroupInvitiationState.UNREGISTERED
    return GroupInvitiationState.REGISTERED
