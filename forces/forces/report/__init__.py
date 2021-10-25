"""Fluid Forces report module"""

from aioextensions import (
    in_thread,
)
import asyncio
from forces.apis.integrates.api import (
    get_finding,
    get_findings,
    vulns_generator,
)
from forces.report.filters import (
    filter_kind,
    filter_repo,
)
from forces.utils.model import (
    ForcesConfig,
)
import oyaml as yaml
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
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


def get_exploitability_measure(score: int) -> str:
    data = {
        "0.91": "Unproven",
        "0.94": "Proof of concept",
        "0.97": "Functional",
        "1.0": "High",
    }
    return data.get(str(score), "-")


def style_report(key: str, value: str) -> str:
    style_data = {
        "title": "[yellow]",
        "state": {"open": "[red]", "closed": "[green]"},
        "exploitability": {
            "Unproven": "[green]",
            "Proof of concept": "[yellow3]",
            "Functional": "[orange3]",
            "High": "[red]",
        },
        "type": {"DAST": "[thistle3]", "SAST": "[light_steel_blue1]"},
    }
    if key in style_data:
        value_style = style_data[key]
        if isinstance(value_style, Dict):
            if value in value_style:
                return f"{value_style[value]}{value}[/]"
            return value
        return f"{value_style}{value}[/]"
    return value


def style_summary(key: str, value: int) -> str:
    markup: str = ""
    if key == "accepted":
        return str(value)
    if key == "open":
        if value == 0:
            markup = "[green]"
        elif value < 10:
            markup = "[yellow3]"
        elif value < 20:
            markup = "[orange3]"
        else:
            markup = "[red]"
    elif key == "closed":
        markup = "[green]"
    return f"{markup}{str(value)}[/]"


async def create_findings_dict(
    group: str,
    **kwargs: str,
) -> Dict[str, Dict[str, Any]]:
    """Returns a dictionary containing as key the findings of a project."""
    findings_dict: Dict[str, Dict[str, Any]] = {}
    findings_futures = [
        get_finding(fin) for fin in await get_findings(group, **kwargs)
    ]
    for _find in asyncio.as_completed(findings_futures):
        find: Dict[str, Any] = await _find
        severity: Dict[str, Any] = find.pop("severity", {})
        find["exploitability"] = severity.get("exploitability", 0)
        find["severity"] = find.pop("severityScore", "N/A")
        findings_dict[find["id"]] = find
        findings_dict[find["id"]].update(
            {"open": 0, "closed": 0, "accepted": 0}
        )
        findings_dict[find["id"]]["vulnerabilities"] = []
    return findings_dict


def format_summary_report(summary: Dict[str, Any], kind: str) -> Table:
    footer = summary.pop("total")
    time_elapsed = summary.pop("time")
    summary_table = Table(
        title="Summary",
        show_header=False,
        highlight=True,
        box=MINIMAL,
        border_style="blue",
        width=40,
        caption=f"Total: {footer} finding(s)\nTime elapsed: {time_elapsed}",
    )
    summary_table.add_column("Vuln state", style="cyan")
    if kind != "all":
        summary_table.add_column("Value")
        for vuln_state, vuln_type in summary.items():
            for key, value in vuln_type.items():
                summary_table.add_row(
                    vuln_state,
                    style_summary(vuln_state, value),
                    end_section=key == "total",
                )
    else:
        summary_table.add_column("Vuln type", style="magenta1")
        summary_table.add_column("Value")
        for vuln_state, vuln_type in summary.items():
            label: Optional[str] = vuln_state
            for key, value in vuln_type.items():
                summary_table.add_row(
                    label,
                    key,
                    style_summary(vuln_state, value),
                    end_section=key == "total",
                )
                label = None
    return summary_table


def format_vuln_table(vulns: List[Dict[str, str]]) -> Table:
    vuln_table = Table(
        show_header=False,
        highlight=True,
        box=MINIMAL,
        border_style="gold1",
        width=60,
    )
    vuln_table.add_column("Vuln attr", style="cyan")
    vuln_table.add_column(
        "Vuln attr values", style="honeydew2", overflow="fold"
    )
    for vuln in vulns:
        for key, value in vuln.items():
            vuln_table.add_row(
                key,
                style_report(key, value),
                end_section=key == "exploitability",
            )
    return vuln_table


def format_rich_report(
    report: Dict[str, Any],
    verbose_level: int,
    kind: str,
) -> Tuple[Table, Table]:
    report_table = Table(
        title="Findings Report",
        show_header=False,
        highlight=True,
        box=MINIMAL,
        width=80,
        border_style="gold1",
    )
    last_key: str = "accepted" if verbose_level == 1 else "vulnerabilities"
    report_table.add_column("Key", style="cyan")
    report_table.add_column("Value")
    findings = report["findings"]
    for find in findings:
        for key, value in find.items():
            if key == "vulnerabilities":
                vuln_data: Union[Table, str] = ""
                if len(value):
                    vuln_data = format_vuln_table(value)
                elif verbose_level == 2:
                    vuln_data = "None currently open"
                elif verbose_level == 3:
                    vuln_data = "None currently open or closed"
                else:  # 4th verbosity level
                    vuln_data = "None currently open, closed or accepted"
                report_table.add_row(key, vuln_data, end_section=True)
            else:
                report_table.add_row(
                    key,
                    style_report(key, str(value)),
                    end_section=key == last_key,
                )
    summary = report["summary"]
    summary_table = format_summary_report(summary, kind)
    return report_table, summary_table


async def generate_report_log(
    report: Dict[str, Any],
    verbose_level: int,
) -> str:
    # Set finding exploitability level
    for finding in report["findings"]:
        finding.pop("id")
        explot = get_exploitability_measure(finding.get("exploitability", 0))
        finding["exploitability"] = explot
        for vuln in finding["vulnerabilities"]:
            vuln["exploitability"] = explot
    # Filter findings without vulnerabilities
    report["findings"] = [
        finding for finding in report["findings"] if finding["vulnerabilities"]
    ]

    if verbose_level == 1:
        # Filter level 1, do not show vulnerabilities details
        for finding in report["findings"]:
            finding.pop("vulnerabilities")
    elif verbose_level == 2:
        # Filter level 2, only show open vulnerabilities
        for finding in report["findings"]:
            finding["vulnerabilities"] = [
                vuln
                for vuln in finding["vulnerabilities"]
                if vuln["state"] == "open"
            ]
    elif verbose_level == 3:
        # Filter level 3, only show open and closed vulnerabilities
        for finding in report["findings"]:
            finding["vulnerabilities"] = [
                vuln
                for vuln in finding["vulnerabilities"]
                if vuln["state"] in ("open", "closed")
            ]
    # If filter level is 4 show accepted, open and closed vulnerabilities
    return await in_thread(yaml.dump, report, allow_unicode=True)


def get_summary_template(kind: str) -> Dict[str, Dict[str, int]]:
    _summary_dict: Dict[str, Dict[str, int]] = {
        "open": {"total": 0},
        "closed": {"total": 0},
        "accepted": {"total": 0},
    }

    return (
        _summary_dict
        if kind != "all"
        else {key: {"DAST": 0, "SAST": 0, "total": 0} for key in _summary_dict}
    )


async def generate_report(
    config: ForcesConfig,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Generate a group vulnerability report.

    :param group: Group Name.
    :param verbose_level: Level of detail of the report.
    """
    _start_time = timer()
    kind = config.kind.value
    repo_name = config.repository_name

    _summary_dict = get_summary_template(kind)

    raw_report: Dict[str, List[Any]] = {"findings": []}
    findings_dict = await create_findings_dict(
        config.group,
        **kwargs,
    )

    async for vuln in vulns_generator(config.group, **kwargs):
        find_id: str = vuln["findingId"]  # type: ignore
        state: str = vuln["currentState"]  # type: ignore

        if not filter_kind(vuln, kind):
            continue
        if config.repository_name and not filter_repo(vuln, kind, repo_name):
            continue

        vuln_type = "SAST" if vuln["vulnerabilityType"] == "lines" else "DAST"

        _summary_dict[state]["total"] += 1
        if kind == "all":
            _summary_dict[state]["DAST"] += bool(vuln_type == "DAST")
            _summary_dict[state]["SAST"] += bool(vuln_type == "SAST")
        findings_dict[find_id][state] += 1

        findings_dict[find_id]["vulnerabilities"].append(
            {
                "type": vuln_type,
                "where": vuln["where"],
                "specific": vuln["specific"],
                "URL": (
                    "https://app.fluidattacks.com/groups/"
                    f'{config.group}/vulns/{vuln["findingId"]}'
                ),
                "state": state,
                "exploitability": findings_dict[find_id]["exploitability"],
            }
        )

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
