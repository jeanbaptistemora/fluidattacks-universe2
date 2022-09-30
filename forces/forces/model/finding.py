# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
)


class FindingSeverity(NamedTuple):
    """Data structure to represent the exploitability data"""

    exploitability: Decimal


class Finding(NamedTuple):
    """Data structure to represent a Finding"""

    id: str
    severity: FindingSeverity
    severity_score: Decimal
    state: str
    title: str
