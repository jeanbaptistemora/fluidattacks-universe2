"""Forces Report module"""

from collections import (
    Counter,
)
from forces.model import (
    Finding,
    ForcesConfig,
    ForcesData,
    ForcesReport,
    KindEnum,
    ReportSummary,
    Vulnerability,
    VulnerabilityState,
)
from forces.report.filters import (
    filter_vulnerabilities,
)
from forces.report.styles import (
    get_exploitability_measure,
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
            vuln_table.add_row(
                "compliance",
                style_report(
                    "compliance",
                    "Compliant" if vuln.compliance else "No, breaks build",
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
        )
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
        if filtered_vulns:
            report_table = format_finding_table(
                config, finding, filtered_vulns, report_table
            )

    summary_table = format_summary_report(report.summary, config.kind)
    return ForcesReport(
        findings_report=report_table, summary_report=summary_table
    )
