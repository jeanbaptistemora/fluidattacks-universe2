"""Forces Report module"""

from forces.model import (
    ForcesConfig,
    ForcesData,
    ForcesReport,
)
from forces.report.filters import (
    filter_vulnerabilities,
)
from forces.report.tables import (
    format_finding_table,
    format_summary_report,
)
from rich.box import (
    MINIMAL,
)
from rich.table import (
    Table,
)


def format_forces_report(
    config: ForcesConfig,
    report: ForcesData,
) -> ForcesReport:
    """Formats the report data into the table & summary seen on Forces
    executions

    Args:
        `config (ForcesConfig)`: Valid Forces config
        `report (ForcesData)`: A tuple containing the list of findings and
        summary data of an ARM group

    Returns:
        `ForcesReport`: A rich-formatted table containing the reported data
        of findings and associated vulns of an ARM group
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
