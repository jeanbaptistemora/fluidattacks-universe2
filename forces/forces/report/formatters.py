# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import asyncio
from forces.apis.integrates.api import (
    get_finding,
    get_findings,
)
from forces.model import (
    Finding,
)
from typing import (
    Any,
)


async def create_findings_dict(
    group: str,
    **kwargs: str,
) -> dict[str, dict[str, Any]]:
    """Returns a dictionary containing as key the findings of a project."""
    findings_dict: dict[str, dict[str, Any]] = {}
    findings_futures = [
        get_finding(fin) for fin in await get_findings(group, **kwargs)
    ]
    for _find in asyncio.as_completed(findings_futures):
        find: dict[str, Any] = await _find
        severity: dict[str, Any] = find.pop("severity", {})
        find["exploitability"] = severity.get("exploitability", 0)
        find["severity"] = find.pop("severityScore", "N/A")
        findings_dict[find["id"]] = find
        findings_dict[find["id"]].update(
            {"open": 0, "closed": 0, "accepted": 0}
        )
        findings_dict[find["id"]]["vulnerabilities"] = []
    return findings_dict


async def gather_finding_data(
    group: str,
    **kwargs: str,
) -> dict[str, Finding]:
    """Returns the findings data needed for the report"""
    findings_dict: dict[str, Finding] = {}
    findings_futures = [
        get_finding(fin) for fin in await get_findings(group, **kwargs)
    ]
    for _find in asyncio.as_completed(findings_futures):
        find: dict[str, Any] = await _find
        severity: dict[str, Any] = find.pop("severity", {})
        find["exploitability"] = severity.get("exploitability", 0)
        findings_dict[find["id"]] = Finding(
            identifier=find["id"],
            title=find["title"],
            state=find["state"],
            exploitability=find["exploitability"],
            severity_score=find["severityScore"],
        )
    return findings_dict


def get_exploitability_measure(score: int) -> str:
    data = {
        "0.91": "Unproven",
        "0.94": "Proof of concept",
        "0.97": "Functional",
        "1.0": "High",
    }
    return data.get(str(score), "-")
