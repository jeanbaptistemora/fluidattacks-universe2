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
    ForcesConfig,
    ForcesReport,
    KindEnum,
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


def style_report(key: str, value: str) -> str:
    """Adds styles as rich console markup to the report values"""
    style_data = {
        "title": "[yellow]",
        "state": {
            VulnerabilityState.OPEN: "[red]",
            VulnerabilityState.CLOSED: "[green]",
        },
        "exploit": {
            "Unproven": "[green]",
            "Proof of concept": "[yellow3]",
            "Functional": "[orange3]",
            "High": "[red]",
        },
        "type": {
            VulnerabilityType.DAST: "[thistle3]",
            VulnerabilityType.SAST: "[light_steel_blue1]",
        },
    }
    if key in style_data:
        value_style = style_data[key]
        if isinstance(value_style, dict):
            if value in value_style:
                return f"{value_style[value]}{value}[/]"
            return value
        return f"{value_style}{value}[/]"
    return str(value)


def style_summary(key: VulnerabilityState, value: int) -> str:
    """Adds styles as rich console markup to the summary values"""
    markup: str = ""
    if key == VulnerabilityState.ACCEPTED:
        return str(value)
    if key == VulnerabilityState.OPEN:
        if value == 0:
            markup = "[green]"
        elif value < 10:
            markup = "[yellow3]"
        elif value < 20:
            markup = "[orange3]"
        else:
            markup = "[red]"
    elif key == VulnerabilityState.CLOSED:
        markup = "[green]"
    return f"{markup}{str(value)}[/]"


def format_summary_report(
    summary: dict[VulnerabilityState | str, Any], kind: KindEnum
) -> Table:
    """Helper method to create the findings summary table from the report's
    summary data\n
    @param `summary`: A dictionary with the summary data\n
    @param `kind`: A kind from the `KindEnum`, can be `ALL`, `STATIC` or
    `DYNAMIC`"""
    total: str = summary.pop("total")
    time_elapsed: str = summary.pop("time")
    summary_table = Table(
        title="Summary",
        show_header=False,
        highlight=True,
        box=MINIMAL,
        border_style="blue",
        width=35,
        caption=f"Total: {total} finding(s)\nTime elapsed: {time_elapsed}",
    )
    # open, closed and/or accepted
    summary_table.add_column("Vuln state", style="cyan")
    if kind == KindEnum.ALL:
        # DAST, SAST and total vulns
        summary_table.add_column("Vuln type", style="magenta1")
        summary_table.add_column("Value")
        for vuln_state, vuln_type in summary.items():
            label: VulnerabilityState | None = vuln_state  # type: ignore
            for key, value in vuln_type.items():
                summary_table.add_row(
                    label,
                    key,
                    style_summary(vuln_state, value),  # type: ignore
                    end_section=key == "total",
                )
                # Blank label from now on to avoid redundancy
                label = None
    # dynamic or static flags were set
    else:
        # No need for a type column, they all have the same
        summary_table.add_column("Value")
        for vuln_state, vuln_type in summary.items():
            for key, value in vuln_type.items():
                summary_table.add_row(
                    vuln_state,
                    style_summary(vuln_state, value),  # type: ignore
                    end_section=key == "total",
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
    report: dict[str, Any],
    verbose_level: int,
    kind: KindEnum,
) -> ForcesReport:
    """Outputs a rich-formatted table containing the reported data of findings
    and associated vulns of an ASM group\n
    @param `report`: A dict containing the list of findings and summary data of
    an ASM group\n
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
    findings = report["findings"]
    for find in findings:
        if find["vulnerabilities"]:
            find_summary: Counter = Counter(
                [vuln.state for vuln in find["vulnerabilities"]]
            )
            for key in (
                "title",
                "state",
                "exploitability",
                "severity",
                *VulnerabilityState,
                "vulnerabilities",
            ):
                value = {**find | find_summary}[key]
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
                            else str(value),
                        ),
                        end_section=key == last_key,
                    )
    # Summary report table
    summary = report["summary"]
    summary_table = format_summary_report(summary, kind)
    return ForcesReport(findings_report=report_table, summary=summary_table)


def get_summary_template(
    kind: KindEnum,
) -> dict[str | VulnerabilityState, dict[str, int]]:
    _summary_dict: dict[str | VulnerabilityState, dict[str, int]] = {
        VulnerabilityState.OPEN: {"total": 0},
        VulnerabilityState.CLOSED: {"total": 0},
        VulnerabilityState.ACCEPTED: {"total": 0},
    }

    return (
        _summary_dict
        if kind != KindEnum.ALL
        else {key: {"DAST": 0, "SAST": 0, "total": 0} for key in _summary_dict}
    )


async def generate_raw_report(
    config: ForcesConfig,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Generate a group vulnerability report.

    :param `group`: Group Name
    """
    _start_time: float = timer()

    _summary_dict = get_summary_template(config.kind)

    raw_report: dict[str, list[Any]] = {"findings": []}
    findings_dict = await create_findings_dict(
        config.group,
        **kwargs,
    )

    async for vuln in vulns_generator(config.group, **kwargs):
        find_id: str = str(vuln["findingId"])
        exploitability: float = float(findings_dict[find_id]["exploitability"])
        findings_dict[find_id]["exploitability"] = exploitability

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
                f'{config.group}/vulns/{vuln["findingId"]}'
            ),
            state=VulnerabilityState[str(vuln["currentState"]).upper()],
            severity=float(str(vuln["severity"]))
            if vuln["severity"] is not None
            else None,
            report_date=str(vuln["reportDate"]),
            exploitability=exploitability,
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
        if config.kind == KindEnum.ALL:
            _summary_dict[vulnerability.state]["DAST"] += bool(
                vulnerability.type == VulnerabilityType.DAST
            )
            _summary_dict[vulnerability.state]["SAST"] += bool(
                vulnerability.type == VulnerabilityType.SAST
            )
        findings_dict[find_id][vulnerability.state] += 1

        findings_dict[find_id]["vulnerabilities"].append(vulnerability)

    for find in findings_dict.values():
        raw_report["findings"].append(find)

    summary = {
        "summary": {
            "total": _summary_dict["open"]["total"]
            + _summary_dict["closed"]["total"]
            + _summary_dict["accepted"]["total"],
            **_summary_dict,
            "time": f"{(timer() - _start_time):.4f} seconds",
        }
    }
    raw_report.update(summary)  # type: ignore
    return raw_report
