# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from decimal import (
    Decimal,
)
from typing import (
    NamedTuple,
)


class Finding(NamedTuple):
    """Data structure to represent a Finding"""

    id: str
    title: str
    state: str
    exploitability: Decimal
    severity_score: Decimal
