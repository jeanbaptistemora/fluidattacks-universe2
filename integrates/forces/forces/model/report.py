from forces.model.finding import (
    Finding,
)
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
    vulnerable: SummaryItem
    safe: SummaryItem
    accepted: SummaryItem
    elapsed_time: str
    total: int


class ForcesData(NamedTuple):
    findings: tuple[Finding, ...]
    summary: ReportSummary


class ForcesReport(NamedTuple):
    findings_report: Table
    summary_report: Table
