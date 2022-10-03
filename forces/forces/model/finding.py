# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from forces.model.vulnerability import (
    Vulnerability,
)
from typing import (
    Tuple,
)


@dataclass
class FindingSummary:
    open: int = 0
    closed: int = 0
    accepted: int = 0


@dataclass
class Finding:
    """Data structure to represent a Finding"""

    identifier: str
    title: str
    state: str
    exploitability: float
    severity_score: float
    summary: FindingSummary = FindingSummary()
    vulnerabilities: Tuple[Vulnerability, ...] = tuple()
