# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
    Set,
)


class OrgFindingPolicy(NamedTuple):
    id: str
    last_status_update: str
    name: str
    status: str
    tags: Set[str]
