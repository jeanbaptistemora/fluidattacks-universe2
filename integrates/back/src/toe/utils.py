# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from typing import (
    Optional,
)


def get_has_vulnerabilities(
    be_present: bool,
    has_vulnerabilities: Optional[bool],
) -> bool:
    return False if be_present is False else has_vulnerabilities or False
