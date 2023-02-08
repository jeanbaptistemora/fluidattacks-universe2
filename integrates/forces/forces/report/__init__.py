"""Forces Report module"""

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
    Finding,
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
    # vulnerable, safe and accepted
    summary_table.add_column("Vuln state", style="cyan")
    if kind == KindEnum.ALL:
        # DAST, SAST and total vulns for each
        summary_table.add_column("Vuln type", style="magenta1")
        summary_table.add_column("Value")
        for state in tuple(VulnerabilityState):
            put_state_label: bool = True
            for vuln_sum in ("DAST", "SAST", "total"):
                summary_table.add_row(
                    state if put_state_label else None,
                    vuln_sum,
                    style_summary(
                        state,  # type: ignore
                        attrgetter(
                            f"{state.value}.{vuln_sum.lower()}"  # type: ignore
                        )(summary),
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
                    state,  # type: ignore
                    attrgetter(f"{state.value}.total")(  # type: ignore
                        summary
                    ),
                ),
                end_section=True,
            )
    return summary_table


def format_vuln_table(
    config: ForcesConfig, vulns: tuple[Vulnerability, ...]
) -> Table:
    """
    Helper method to create the nested vulns table\n
    @param `config`: Forces config
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
        vuln_table.add_row("type", style_report("type", vuln.type))
        vuln_table.add_row("where", style_report("where", vuln.where))
        vuln_table.add_row("specific", style_report("specific", vuln.specific))
        vuln_table.add_row(
            "state",
            style_report("state", vuln.state),
            end_section=not config.strict,
        )
        if config.strict:
            compliance = check_policy_compliance(config, vuln)
            vuln_table.add_row(
                "compliance",
                style_report(
                    "compliance",
                    "Compliant" if compliance else "No, breaks build",
                ),
                end_section=True,
            )
    return vuln_table


def format_finding_table(
    config: ForcesConfig,
    finding: Finding,
    filtered_vulns: tuple[Vulnerability, ...],
    table: Table,
) -> Table:
    finding_summary: Counter = Counter(
        [vuln.state for vuln in finding.vulnerabilities]
    )
    table.add_row("title", style_report("title", finding.title))
    table.add_row("URL", finding.url)
    table.add_row("state", style_report("state", finding.state))
    table.add_row(
        "exploit",
        style_report(
            "exploit", get_exploitability_measure(finding.exploitability)
        ),
    )
    table.add_row("severity", style_report("severity", str(finding.severity)))
    for vuln_state in tuple(VulnerabilityState):
        table.add_row(
            vuln_state,
            style_report(vuln_state, str(finding_summary[vuln_state])),
            end_section=vuln_state == VulnerabilityState.ACCEPTED
            and config.verbose_level == 1,
        )
    if config.verbose_level != 1:
        vulns_data: Table = format_vuln_table(config, filtered_vulns)
        table.add_row("vulns", vulns_data, end_section=True)

    return table


def format_rich_report(
    config: ForcesConfig,
    report: ForcesData,
) -> ForcesReport:
    """Outputs a rich-formatted table containing the reported data of findings
    and associated vulns of an ARM group\n
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
    report_table.add_column("Attributes", style="cyan")
    report_table.add_column("Data", overflow="fold")
    for finding in report.findings:
        filtered_vulns = filter_vulnerabilities(
            finding.vulnerabilities, config.verbose_level
        )
        if filtered_vulns or config.verbose_level == 1:
            report_table = format_finding_table(
                config, finding, filtered_vulns, report_table
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
        VulnerabilityState.VULNERABLE: {"DAST": 0, "SAST": 0, "total": 0},
        VulnerabilityState.SAFE: {"DAST": 0, "SAST": 0, "total": 0},
        VulnerabilityState.ACCEPTED: {"DAST": 0, "SAST": 0, "total": 0},
    }
    findings_dict = await create_findings_dict(
        organization=config.organization,
        group=config.group,
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
            state=VulnerabilityState[str(vuln["state"])],
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
        vulnerable=SummaryItem(
            dast=_summary_dict[VulnerabilityState.VULNERABLE]["DAST"],
            sast=_summary_dict[VulnerabilityState.VULNERABLE]["SAST"],
            total=_summary_dict[VulnerabilityState.VULNERABLE]["total"],
        ),
        safe=SummaryItem(
            dast=_summary_dict[VulnerabilityState.SAFE]["DAST"],
            sast=_summary_dict[VulnerabilityState.SAFE]["SAST"],
            total=_summary_dict[VulnerabilityState.SAFE]["total"],
        ),
        accepted=SummaryItem(
            dast=_summary_dict[VulnerabilityState.ACCEPTED]["DAST"],
            sast=_summary_dict[VulnerabilityState.ACCEPTED]["SAST"],
            total=_summary_dict[VulnerabilityState.ACCEPTED]["total"],
        ),
        total=_summary_dict[VulnerabilityState.VULNERABLE]["total"]
        + _summary_dict[VulnerabilityState.SAFE]["total"]
        + _summary_dict[VulnerabilityState.ACCEPTED]["total"],
        elapsed_time=f"{(timer() - _start_time):.4f} seconds",
    )

    return ForcesData(
        findings=tuple(find for find in findings_dict.values()),
        summary=summary,
    )
