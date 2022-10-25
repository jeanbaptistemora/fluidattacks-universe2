# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from singer_io.singer2.json import (
    JsonObj,
)


@dataclass(frozen=True)
class StabilityTrend:
    data: JsonObj
