# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Maybe,
)


@dataclass(frozen=True)
class EtlState:
    # check results
    results_recent: Maybe[datetime]
    results_oldest: Maybe[datetime]
