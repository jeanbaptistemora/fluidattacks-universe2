# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

"""Fluid Forces report module"""

from collections import (
    Counter,
)
from forces.apis.integrates.api import (
    vulns_generator,
)
from forces.model import (
    Finding,
    ForcesConfig,
    ForcesReport,
    KindEnum,
    ReportSummary,
    SummaryItem,
    Vulnerability,
    VulnerabilityState,
    VulnerabilityType,
)
from forces.report.filters import (
    filter_kind,
    filter_repo,
    filter_vulnerabilities,
)
from forces.report.formatters import (
    create_findings_dict,
    get_exploitability_measure,
)
from forces.report.styles import (
    style_report,
    style_summary,
)
from operator import (
    attrgetter,
)
from rich.box import (
    MINIMAL,
)
from rich.table import (
    Table,
)
from timeit import (
    default_timer as timer,
)
from typing import (
    Any,
)


def format_summary_report(summary: ReportSummary, kind: KindEnum) -> Table:
    """Helper method to create the findings summary table from the report's
    summary data\n
    @param `summary`: A dictionary with the summary data\n
    @param `kind`: A kind from the `KindEnum`, can be `ALL`, `STATIC` or
    `DYNAMIC`"""
    summary_table = Table(
        title="Summary",
        show_header=False,
        highlight=True,
        box=MINIMAL,
        border_style="blue",
        width=35,
        caption=(
            f"Total: {summary.total} vulnerabilities\n"
            f"Elapsed time: {summary.elapsed_time}"
        ),
    )
    # open, closed and/or accepted
    summary_table.add_column("Vuln state", style="cyan")
    if kind == KindEnum.ALL:
        # DAST, SAST and total vulns
        summary_table.add_column("Vuln type", style="magenta1")
        summary_table.add_column("Value")
        for state in tuple(VulnerabilityState):
            put_state_label: bool = True
            for vuln_sum in ("DAST", "SAST", "total"):
                summary_table.add_row(
                    state if put_state_label else None,
                    vuln_sum,
                    style_summary(
                        state,
                        attrgetter(f"{state.value}.{vuln_sum.lower()}")(
                            summary
                        ),
                    ),
                    end_section=vuln_sum == "total",
                )
                put_state_label = False
    else:
        summary_table.add_column("Value")
        for state in tuple(VulnerabilityState):
            summary_table.add_row(
                state,
                style_summary(
                    state, attrgetter(f"{state.value}.total")(summary)
                ),
                end_section=True,
            )
    return summary_table


def format_vuln_table(vulns: tuple[Vulnerability, ...]) -> Table:
    """
    Helper method to create the nested vulns table\n
    @param `vulns`: A list of dicts with each vuln's data
    """
    vuln_table = Table(
        show_header=False,
        highlight=True,
        box=MINIMAL,
        border_style="gold1",
    )
    vuln_table.add_column("Vuln attr", style="cyan")
    vuln_table.add_column(
        "Vuln attr values", style="honeydew2", overflow="fold"
    )
    for vuln in vulns:
        for key in ("type", "where", "specific", "URL", "state"):
            vuln_table.add_row(
                key,
                style_report(key, attrgetter(key.lower())(vuln)),
                end_section=key == "state",
            )
    return vuln_table


def format_rich_report(
    report: dict[str, list[Finding] | ReportSummary],
    verbose_level: int,
    kind: KindEnum,
) -> ForcesReport:
    """Outputs a rich-formatted table containing the reported data of findings
    and associated vulns of an ASM group\n
    @param `report`: A dict containing the list of findings and summary data of
    an ARM group\n
    @param `verbose_level`: An int from 1 to 4 of the desired verbosity level,
    with more data being shown the higher the number\n
    @param `kind`: A kind from the `KindEnum`, can be
    `ALL`, `STATIC` or `DYNAMIC`
    """
    # Finding report table
    report_table = Table(
        title="Findings Report",
        show_header=False,
        highlight=True,
        box=MINIMAL,
        width=80,
        border_style="gold1",
    )
    last_key: str = "accepted" if verbose_level == 1 else "vulnerabilities"
    report_table.add_column("Attributes", style="cyan")
    report_table.add_column("Data")
    findings: list[Finding] = report["findings"]  # type: ignore
    for find in findings:
        if find.vulnerabilities:
            find_summary: Counter = Counter(
                [vuln.state for vuln in find.vulnerabilities]
            )
            for key in (
                "title",
                "state",
                "exploitability",
                "severity",
                *VulnerabilityState,
                "vulnerabilities",
            ):
                value = (
                    find_summary[key]
                    if key in set(VulnerabilityState)
                    else attrgetter(key)(find)
                )
                if is_exploit := key == "exploitability":
                    key = "exploit"

                if key == "vulnerabilities" and verbose_level != 1:
                    filtered_vulns: tuple[
                        Vulnerability, ...
                    ] = filter_vulnerabilities(value, verbose_level)
                    vulns_data: Table | str = ""
                    if filtered_vulns:
                        vulns_data = format_vuln_table(filtered_vulns)
                    elif verbose_level == 2:
                        vulns_data = "None currently open"
                    elif verbose_level == 3:
                        vulns_data = "None currently open or closed"
                    else:
                        vulns_data = "None currently open, closed or accepted"
                    report_table.add_row("vulns", vulns_data, end_section=True)
                elif key != "vulnerabilities":
                    report_table.add_row(
                        key,
                        style_report(
                            key,
                            get_exploitability_measure(value)
                            if is_exploit
                            else value,
                        ),
                        end_section=key == last_key,
                    )
    # Summary report table
    summary: ReportSummary = report["summary"]  # type: ignore
    summary_table = format_summary_report(summary, kind)
    return ForcesReport(findings_report=report_table, summary=summary_table)


async def generate_raw_report(
    config: ForcesConfig,
    **kwargs: Any,
) -> dict[str, list[Finding] | ReportSummary]:
    """
    Generate a group vulnerability report.

    :param `group`: Group Name
    """
    _start_time: float = timer()

    raw_report: dict[str, list[Finding] | ReportSummary] = {"findings": []}
    _summary_dict: dict[VulnerabilityState, dict[str, int]] = {
        VulnerabilityState.OPEN: {"DAST": 0, "SAST": 0, "total": 0},
        VulnerabilityState.CLOSED: {"DAST": 0, "SAST": 0, "total": 0},
        VulnerabilityState.ACCEPTED: {"DAST": 0, "SAST": 0, "total": 0},
    }

    findings_dict = await create_findings_dict(
        config.group,
        **kwargs,
    )

    async for vuln in vulns_generator(config.group, **kwargs):
        find_id: str = str(vuln["findingId"])

        vulnerability: Vulnerability = Vulnerability(
            type=(
                VulnerabilityType.SAST
                if vuln["vulnerabilityType"] == "lines"
                else VulnerabilityType.DAST
            ),
            where=str(vuln["where"]),
            specific=str(vuln["specific"]),
            url=(
                "https://app.fluidattacks.com/groups/"
                f"{config.group}/vulns/{find_id}"
            ),
            state=VulnerabilityState[str(vuln["currentState"]).upper()],
            severity=float(str(vuln["severity"]))
            if vuln["severity"] is not None
            else None,
            report_date=str(vuln["reportDate"]),
            exploitability=findings_dict[find_id].exploitability,
            root_nickname=str(vuln["rootNickname"])
            if vuln.get("rootNickName")
            else None,
        )

        if not filter_kind(vulnerability, config.kind):
            continue
        if config.repository_name and not filter_repo(
            vulnerability, config.kind, config.repository_name
        ):
            continue

        _summary_dict[vulnerability.state]["total"] += 1
        _summary_dict[vulnerability.state]["DAST"] += bool(
            vulnerability.type == VulnerabilityType.DAST
        )
        _summary_dict[vulnerability.state]["SAST"] += bool(
            vulnerability.type == VulnerabilityType.SAST
        )

        findings_dict[find_id].vulnerabilities.append(vulnerability)

    for find in findings_dict.values():
        raw_report["findings"].append(find)  # type: ignore

    raw_report["summary"] = ReportSummary(
        open=SummaryItem(
            dast=_summary_dict[VulnerabilityState.OPEN]["DAST"],
            sast=_summary_dict[VulnerabilityState.OPEN]["SAST"],
            total=_summary_dict[VulnerabilityState.OPEN]["total"],
        ),
        closed=SummaryItem(
            dast=_summary_dict[VulnerabilityState.CLOSED]["DAST"],
            sast=_summary_dict[VulnerabilityState.CLOSED]["SAST"],
            total=_summary_dict[VulnerabilityState.CLOSED]["total"],
        ),
        accepted=SummaryItem(
            dast=_summary_dict[VulnerabilityState.ACCEPTED]["DAST"],
            sast=_summary_dict[VulnerabilityState.ACCEPTED]["SAST"],
            total=_summary_dict[VulnerabilityState.ACCEPTED]["total"],
        ),
        total=_summary_dict[VulnerabilityState.OPEN]["total"]
        + _summary_dict[VulnerabilityState.CLOSED]["total"]
        + _summary_dict[VulnerabilityState.ACCEPTED]["total"],
        elapsed_time=f"{(timer() - _start_time):.4f} seconds",
    )

    return raw_report
