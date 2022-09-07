# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dynamodb.types import (
    Item,
)


def get_full_name(stakeholder_info: dict[str, str]) -> str:
    return str.join(
        " ",
        [
            stakeholder_info.get("first_name", ""),
            stakeholder_info.get("last_name", ""),
        ],
    )


def format_invitation_state(invitation: Item, is_registered: bool) -> str:
    if invitation and not invitation["is_used"]:
        return "PENDING"
    if not is_registered:
        return "UNREGISTERED"
    return "REGISTERED"
