# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    NamedTuple,
    Optional,
)


class Advisory(NamedTuple):
    associated_advisory: str
    package_name: str
    package_manager: str
    vulnerable_version: str
    source: str
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    severity: Optional[str] = None
