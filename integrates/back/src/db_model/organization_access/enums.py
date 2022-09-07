# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)


class OrganizationInvitiationState(str, Enum):
    PENDING: str = "PENDING"
    UNREGISTERED: str = "UNREGISTERED"
    REGISTERED: str = "REGISTERED"
