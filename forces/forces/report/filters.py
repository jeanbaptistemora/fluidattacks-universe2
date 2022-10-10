# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import fnmatch
from forces.model import (
    KindEnum,
    VulnerabilityState,
    VulnerabilityType,
)
from typing import (
    Any,
    cast,
)


def filter_kind(
    vuln: dict[str, Any],
    kind: KindEnum,
) -> bool:
    vuln_type = (
        VulnerabilityType.SAST
        if vuln["vulnerabilityType"] == "lines"
        else VulnerabilityType.DAST
    )
    return (
        (kind == KindEnum.DYNAMIC and vuln_type == VulnerabilityType.DAST)
        or (kind == KindEnum.STATIC and vuln_type == VulnerabilityType.SAST)
        or kind == KindEnum.ALL
    )


def filter_repo(
    vuln: dict[str, Any],
    kind: KindEnum,
    repo_name: str | None = None,
) -> bool:
    vuln_type: VulnerabilityType = (
        VulnerabilityType.SAST
        if vuln["vulnerabilityType"] == "lines"
        else VulnerabilityType.DAST
    )

    if (
        kind in (KindEnum.ALL, KindEnum.STATIC)
        and vuln_type == VulnerabilityType.SAST
        and repo_name
    ):
        return fnmatch.fnmatch(cast(str, vuln["where"]), f"{repo_name}/*")
    if (
        kind in (KindEnum.ALL, KindEnum.DYNAMIC)
        and vuln_type == VulnerabilityType.DAST
    ):
        root_nickname: str | None = vuln.get("rootNickname", "")
        return root_nickname == repo_name or not root_nickname
    return True


def filter_report(
    report: dict[str, Any],
    verbose_level: int,
) -> dict[str, Any]:
    # Set finding exploitability level
    for finding in report["findings"]:
        finding.pop("id")
    # Filter findings without vulnerabilities
    report["findings"] = [
        finding for finding in report["findings"] if finding["vulnerabilities"]
    ]

    # Remove extra info not needed for the formatted report
    if verbose_level == 1:
        # Filter level 1, do not show vulnerabilities details
        filter_vulns(report["findings"], set())
    elif verbose_level == 2:
        # Filter level 2, only show open vulnerabilities
        filter_vulns(report["findings"], {VulnerabilityState.OPEN})
    elif verbose_level == 3:
        # Filter level 3, only show open and closed vulnerabilities
        filter_vulns(
            report["findings"],
            {VulnerabilityState.OPEN, VulnerabilityState.CLOSED},
        )
    else:
        # If filter level is 4 show open, closed and accepted vulnerabilities
        filter_vulns(report["findings"], set(VulnerabilityState))
    return report


def filter_vulns(
    findings: list[dict[str, Any]],
    allowed_vuln_states: set[VulnerabilityState],
) -> list[dict[str, Any]]:
    """Helper method to filter vulns in findings based on the requested vuln
    states set by the verbosity level of the report"""
    # Verbosity level of 1
    if allowed_vuln_states == set():
        for finding in findings:
            finding.pop("vulnerabilities")
    # Verbosity levels of 2, 3 and 4
    else:
        for finding in findings:
            finding["vulnerabilities"] = tuple(
                filter(
                    lambda vuln: vuln.state in allowed_vuln_states,
                    finding["vulnerabilities"],
                )
            )
    return findings
