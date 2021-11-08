from aioextensions import (
    run,
)
from charts import (
    utils,
)
from charts.types import (
    RemediationReport,
)
from custom_types import (
    Vulnerability as VulnerabilityType,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score,
)
from typing import (
    Dict,
    List,
    Tuple,
)


def had_state_by_then(
    *,
    last_day: datetime,
    findings_cvssf: Dict[str, Decimal],
    state: str,
    vulnerability: VulnerabilityType,
) -> Decimal:
    historic_state = reversed(vulnerability["historic_state"])
    last_state: dict = next(
        filter(
            lambda item: datetime.strptime(item["date"], "%Y-%m-%d %H:%M:%S")
            <= last_day,
            historic_state,
        ),
        {},
    )

    return (
        findings_cvssf[str(vulnerability["finding_id"])]
        if last_state.get("state") == state
        else Decimal("0.0")
    )


def get_totals_by_week(
    *,
    vulnerabilities: List[VulnerabilityType],
    findings_cvssf: Dict[str, Decimal],
    last_day: datetime,
) -> Tuple[Decimal, Decimal]:
    open_vulnerabilities = Decimal(
        sum(
            had_state_by_then(
                last_day=last_day,
                state="open",
                vulnerability=vulnerability,
                findings_cvssf=findings_cvssf,
            )
            for vulnerability in vulnerabilities
        )
    )
    closed_vulnerabilities = Decimal(
        sum(
            had_state_by_then(
                last_day=last_day,
                state="closed",
                vulnerability=vulnerability,
                findings_cvssf=findings_cvssf,
            )
            for vulnerability in vulnerabilities
        )
    )

    return open_vulnerabilities, closed_vulnerabilities


async def generate_one(groups: Tuple[str, ...]) -> RemediationReport:
    loaders: Dataloaders = get_new_context()
    groups_findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(groups)
    findings_cvssf: Dict[str, Decimal] = {
        finding.id: utils.get_cvssf(get_severity_score(finding.severity))
        for group_findings in groups_findings
        for finding in group_findings
    }
    finding_ids = [
        finding.id
        for group_findings in groups_findings
        for finding in group_findings
    ]

    current_rolling_week = datetime.now()
    previous_rolling_week = current_rolling_week - timedelta(days=7)

    vulnerabilities: List[
        VulnerabilityType
    ] = await loaders.finding_vulns_nzr.load_many_chained(finding_ids)

    total_previous_open, total_previous_closed = get_totals_by_week(
        vulnerabilities=vulnerabilities,
        findings_cvssf=findings_cvssf,
        last_day=previous_rolling_week,
    )

    total_current_open, total_current_closed = get_totals_by_week(
        vulnerabilities=vulnerabilities,
        findings_cvssf=findings_cvssf,
        last_day=current_rolling_week,
    )

    return {
        "current": {
            "closed": total_current_closed,
            "open": total_current_open,
        },
        "previous": {
            "closed": total_previous_closed,
            "open": total_previous_open,
        },
        "totalGroups": len(groups),
    }


async def generate_all() -> None:
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=await generate_one(org_groups),
            entity="organization",
            subject=org_id,
        )


if __name__ == "__main__":
    run(generate_all())
