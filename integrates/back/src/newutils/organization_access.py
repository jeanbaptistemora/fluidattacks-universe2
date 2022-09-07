# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from db_model.organization_access.enums import (
    OrganizationInvitiationState,
)
from db_model.organization_access.types import (
    OrganizationInvitation,
)
from typing import (
    Optional,
)


def format_invitation_state(
    invitation: Optional[OrganizationInvitation], is_registered: bool
) -> OrganizationInvitiationState:
    if invitation and not invitation.is_used:
        return OrganizationInvitiationState.PENDING
    if not is_registered:
        return OrganizationInvitiationState.UNREGISTERED
    return OrganizationInvitiationState.REGISTERED
