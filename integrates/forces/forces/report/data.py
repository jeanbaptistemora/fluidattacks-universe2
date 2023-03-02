from .filters import (
    filter_kind,
    filter_repo,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from forces.apis.integrates.api import (
    get_findings,
    get_vulnerabilities,
)
from forces.model import (
    Finding,
    FindingState,
    ForcesConfig,
    ForcesData,
    ReportSummary,
    SummaryItem,
    Vulnerability,
    VulnerabilityState,
    VulnerabilityType,
)
from forces.utils.strict_mode import (
    get_policy_compliance,
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


async def get_group_findings_info(
    organization: str,
    group: str,
    **kwargs: str,
) -> dict[str, Finding]:
    """Format the findings of a group into a dictionary

    Args:
        `organization (str)`: Organization name
        `group (str)`: Group name

    Returns:
        `dict[str, Finding]`: A dictionary containing the findings of a group
        with their identifier as key
    """
    findings_dict: dict[str, Finding] = {}
    findings = await get_findings(group, **kwargs)
    for finding in findings:
        severity: dict[str, Any] = finding.pop("severity", {})
        finding["exploitability"] = severity.get("exploitability", 0)

        findings_dict[finding["id"]] = Finding(
            identifier=str(finding["id"]),
            title=str(finding["title"]),
            state=FindingState[str(finding["status"]).upper()],
            exploitability=float(finding["exploitability"]),
            severity=Decimal(str(finding["severityScore"])),
            url=(
                f"https://app.fluidattacks.com/orgs/{organization}/groups/"
                f"{group}/vulns/{finding['id']}"
            ),
            vulnerabilities=[],
        )
    return findings_dict


async def compile_raw_report(
    config: ForcesConfig,
    **kwargs: Any,
) -> ForcesData:
    """Parses and compiles the data needed for the Forces Report.

    Args:
        `config (ForcesConfig)`: Valid Forces config

    Returns:
        `ForcesData`: A namedtuple with the findings data and a summary
    """
    _start_time: float = timer()

    _summary_dict: dict[VulnerabilityState, dict[str, int]] = {
        VulnerabilityState.VULNERABLE: {"DAST": 0, "SAST": 0, "total": 0},
        VulnerabilityState.SAFE: {"DAST": 0, "SAST": 0, "total": 0},
        VulnerabilityState.ACCEPTED: {"DAST": 0, "SAST": 0, "total": 0},
    }
    findings_dict = await get_group_findings_info(
        organization=config.organization,
        group=config.group,
        **kwargs,
    )

    for vuln in await get_vulnerabilities(config, **kwargs):
        find_id: str = str(vuln["findingId"])

        # The API may serve vulns without their corresponding Finding
        if find_id not in findings_dict:
            continue

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
            compliance=get_policy_compliance(
                config=config,
                report_date=datetime.fromisoformat(
                    str(vuln["reportDate"])
                ).replace(tzinfo=ZoneInfo("America/Bogota")),
                severity=Decimal(str(vuln["severity"]))
                if vuln["severity"] is not None
                else findings_dict[find_id].severity,
                state=VulnerabilityState[str(vuln["state"])],
            ),
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
