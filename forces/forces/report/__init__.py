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
from timeit import (
    default_timer as timer,
)
from typing import (
    Any,
    Dict,
    List,
)


def get_exploitability_measure(score: int) -> str:
    data = {
        "0.91": "Unproven",
        "0.94": "Proof of concept",
        "0.97": "Functional",
        "1.0": "High",
    }
    return data.get(str(score), "-")


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


async def generate_report_log(
    report: Dict[str, Any],
    verbose_level: int,
) -> str:
    # Set finding exploitability level
    for finding in report["findings"]:
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
        # Filter level 4, only show open and closed vulnerabilities
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
