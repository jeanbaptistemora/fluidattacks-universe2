# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from ._utils import (
    DateInterval,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Maybe,
)


@dataclass(frozen=True)
class EtlState:
    results: Maybe[DateInterval]  # check results stream
