# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)


class RootStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    INACTIVE: str = "INACTIVE"


class RootType(str, Enum):
    GIT: str = "Git"
    IP: str = "IP"
    URL: str = "URL"
