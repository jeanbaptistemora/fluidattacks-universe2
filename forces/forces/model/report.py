# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from rich.table import (
    Table,
)
from typing import (
    NamedTuple,
)


class SummaryItem(NamedTuple):
    dast: int
    sast: int
    total: int


class ReportSummary(NamedTuple):
    open: SummaryItem
    closed: SummaryItem
    accepted: SummaryItem
    elapsed_time: str
    total: int


class ForcesReport(NamedTuple):
    findings_report: Table
    summary: Table
