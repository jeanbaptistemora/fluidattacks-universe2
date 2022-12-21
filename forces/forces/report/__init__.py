"""Fluid Forces report module"""

from collections import (
    Counter,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from forces.apis.integrates.api import (
    vulns_generator,
)
from forces.model import (
    ForcesConfig,
    ForcesData,
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
from forces.utils.strict_mode import (
    check_policy_compliance,
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
from zoneinfo import (
    ZoneInfo,
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


def format_vuln_table(
    config: ForcesConfig, vulns: tuple[Vulnerability, ...]
) -> Table:
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
        for key in ("type", "where", "specific", "state"):
            vuln_table.add_row(
                key,
                style_report(key, attrgetter(key)(vuln)),
                end_section=False if config.strict else key == "state",
            )
        if config.strict:
            compliance = check_policy_compliance(config, vuln)
            vuln_table.add_row(
                "compliance",
                "[green]Yes[/]" if compliance else "[red]No, breaks build[/]",
                end_section=True,
            )
    return vuln_table


def format_rich_report(
    config: ForcesConfig,
    report: ForcesData,
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
    last_key: str = (
        "accepted" if config.verbose_level == 1 else "vulnerabilities"
    )
    report_table.add_column("Attributes", style="cyan")
    report_table.add_column("Data", overflow="fold")
    for find in report.findings:
        filtered_vulns = filter_vulnerabilities(
            find.vulnerabilities, config.verbose_level
        )
        if filtered_vulns or config.verbose_level == 1:
            find_summary: Counter = Counter(
                [vuln.state for vuln in find.vulnerabilities]
            )
            for key in (
                "title",
                "URL",
                "state",
                "exploitability",
                "severity",
                *VulnerabilityState,
                "vulnerabilities",
            ):
                value = (
                    find_summary[key]
                    if key in set(VulnerabilityState)
                    else attrgetter(str(key).lower())(find)
                )
                if is_exploit := key == "exploitability":
                    key = "exploit"

                if key == "vulnerabilities" and config.verbose_level != 1:
                    vulns_data: Table = format_vuln_table(
                        config, filtered_vulns
                    )
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

    summary_table = format_summary_report(report.summary, config.kind)
    return ForcesReport(
        findings_report=report_table, summary_report=summary_table
    )


async def generate_raw_report(
    config: ForcesConfig,
    **kwargs: Any,
) -> ForcesData:
    """
    Parses and compiles the data needed for the Forces Report.

    @param `config`: Valid Forces Config
    """
    _start_time: float = timer()

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
            state=VulnerabilityState[str(vuln["currentState"]).upper()],
            severity=Decimal(str(vuln["severity"]))
            if vuln["severity"] is not None
            else findings_dict[find_id].severity,
            report_date=datetime.fromisoformat(
                str(vuln["reportDate"])
            ).replace(tzinfo=ZoneInfo("America/Bogota")),
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

    summary = ReportSummary(
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

    return ForcesData(
        findings=tuple(find for find in findings_dict.values()),
        summary=summary,
    )
