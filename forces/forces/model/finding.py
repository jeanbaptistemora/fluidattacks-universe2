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
    OPEN: str = "open"
    CLOSED: str = "closed"


class Finding(NamedTuple):
    identifier: str
    title: str
    state: FindingState
    exploitability: float
    severity: float
    vulnerabilities: list[Vulnerability]
