# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from enum import (
    Enum,
)
from forces.model.vulnerability import (
    Vulnerability,
)
from typing import (
    NamedTuple,
)


class FindingState(str, Enum):
    """Enum to represent the possible Finding states"""

    CLOSED: str = "closed"
    OPEN: str = "open"


class Finding(NamedTuple):
    """Data structure to represent a Finding"""

    identifier: str
    title: str
    state: FindingState
    exploitability: float
    severity: float | str
    vulnerabilities: list[Vulnerability] = []
