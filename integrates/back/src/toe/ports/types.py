# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from typing import (
    NamedTuple,
    Optional,
)


class ToePortAttributesToAdd(NamedTuple):
    be_present: bool
    root_id: str
    attacked_at: Optional[datetime] = None
    attacked_by: Optional[str] = None
    first_attack_at: Optional[datetime] = None
    seen_first_time_by: Optional[str] = None
    has_vulnerabilities: Optional[bool] = None
    seen_at: Optional[datetime] = None
