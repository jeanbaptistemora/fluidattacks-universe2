# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.group_access.enums import (
    GroupInvitiationState,
)
from db_model.group_access.types import (
    GroupInvitation,
)
from typing import (
    Optional,
)


def format_invitation_state(
    invitation: Optional[GroupInvitation], is_registered: bool
) -> GroupInvitiationState:
    if invitation and not invitation.is_used:
        return GroupInvitiationState.PENDING
    if not is_registered:
        return GroupInvitiationState.UNREGISTERED
    return GroupInvitiationState.REGISTERED
