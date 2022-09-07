# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)


class OrganizationStateStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    DELETED: str = "DELETED"
