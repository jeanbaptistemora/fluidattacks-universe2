# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from rich.table import (
    Table,
)
from typing import (
    NamedTuple,
)


class ForcesReport(NamedTuple):
    findings_report: Table
    summary: Table
