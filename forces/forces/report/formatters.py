import asyncio
from decimal import (
    Decimal,
)
from forces.apis.integrates.api import (
    get_finding,
    get_findings,
)
from forces.model import (
    Finding,
    FindingState,
)
from typing import (
    Any,
)


async def create_findings_dict(
    group: str,
    **kwargs: str,
) -> dict[str, Finding]:
    """Returns a dictionary containing as key the findings of a project."""
    findings_dict: dict[str, Finding] = {}
    findings_futures = [
        get_finding(fin) for fin in await get_findings(group, **kwargs)
    ]
    for _find in asyncio.as_completed(findings_futures):
        find: dict[str, Any] = await _find
        severity: dict[str, Any] = find.pop("severity", {})
        find["exploitability"] = severity.get("exploitability", 0)
        findings_dict[find["id"]] = Finding(
            identifier=str(find["id"]),
            title=str(find["title"]),
            state=FindingState[str(find["state"]).upper()],
            exploitability=float(find["exploitability"]),
            severity=Decimal(str(find["severityScore"])),
            url=(
                "https://app.fluidattacks.com/groups/"
                f"{group}/vulns/{find['id']}"
            ),
            vulnerabilities=[],
        )
    return findings_dict


def get_exploitability_measure(score: float) -> str:
    return {
        "0.91": "Unproven",
        "0.94": "Proof of concept",
        "0.97": "Functional",
        "1.0": "High",
    }.get(str(score), "-")


def translate_vuln_state(state: str) -> str:
    return {"open": "vulnerable", "closed": "safe"}.get(state, state)
