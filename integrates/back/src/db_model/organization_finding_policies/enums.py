# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)


class PolicyStateStatus(str, Enum):
    APPROVED: str = "APPROVED"
    INACTIVE: str = "INACTIVE"
    REJECTED: str = "REJECTED"
    SUBMITTED: str = "SUBMITTED"
