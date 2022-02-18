from aioextensions import (
    collect,
    run,
)
from charts import (
    utils,
)
from charts.types import (
    RemediationReport,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from decimal import (
    Decimal,
)
from findings.domain.core import (
    get_severity_score,
)
from more_itertools import (
    chunked,
)
from typing import (
    Dict,
    Optional,
    Tuple,
)


def get_last_state(
    historic_state: Tuple[VulnerabilityState, ...],
    last_day: datetime,
) -> Optional[VulnerabilityState]:
    return next(
        (
            item
            for item in list(reversed(historic_state))
            if datetime.fromisoformat(item.modified_date) <= last_day
        ),
        None,
    )


async def had_state_by_then(
    *,
    last_day: datetime,
    findings_cvssf: Dict[str, Decimal],
    loaders: Dataloaders,
    state: VulnerabilityStateStatus,
    vulnerabilities: Tuple[Vulnerability, ...],
) -> Decimal:

    historics_states: Tuple[
        Tuple[VulnerabilityState, ...], ...
    ] = await loaders.vulnerability_historic_state.load_many(
        tuple(vulnerability.id for vulnerability in vulnerabilities)
    )

    lasts_valid_states: Tuple[Optional[VulnerabilityState], ...] = tuple(
        get_last_state(historic_state, last_day)
        for historic_state in historics_states
    )

    return Decimal(
        sum(
            findings_cvssf[str(vulnerability.finding_id)]
            if last_valid_state and last_valid_state.status == state
            else Decimal("0.0")
            for vulnerability, last_valid_state in zip(
                vulnerabilities, lasts_valid_states
            )
        )
    )


async def get_totals_by_week(
    *,
    vulnerabilities: Tuple[Vulnerability, ...],
    findings_cvssf: Dict[str, Decimal],
    last_day: datetime,
    loaders: Dataloaders,
) -> Tuple[Decimal, Decimal]:
    open_vulnerabilities = sum(
        await collect(
            tuple(
                had_state_by_then(
                    last_day=last_day,
                    loaders=loaders,
                    state=VulnerabilityStateStatus.OPEN,
                    vulnerabilities=chunked_vulnerabilities,
                    findings_cvssf=findings_cvssf,
                )
                for chunked_vulnerabilities in chunked(vulnerabilities, 16)
            ),
            workers=16,
        )
    )

    closed_vulnerabilities = sum(
        await collect(
            tuple(
                had_state_by_then(
                    last_day=last_day,
                    loaders=loaders,
                    state=VulnerabilityStateStatus.CLOSED,
                    vulnerabilities=chunked_vulnerabilities,
                    findings_cvssf=findings_cvssf,
                )
                for chunked_vulnerabilities in chunked(vulnerabilities, 16)
            ),
            workers=16,
        )
    )

    return Decimal(open_vulnerabilities), Decimal(closed_vulnerabilities)


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

    current_rolling_week = datetime.now(tz=timezone.utc)
    previous_rolling_week = current_rolling_week - timedelta(days=7)

    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        finding_ids
    )

    total_previous_open, total_previous_closed = await get_totals_by_week(
        vulnerabilities=vulnerabilities,
        findings_cvssf=findings_cvssf,
        last_day=previous_rolling_week,
        loaders=loaders,
    )

    total_current_open, total_current_closed = await get_totals_by_week(
        vulnerabilities=vulnerabilities,
        findings_cvssf=findings_cvssf,
        last_day=current_rolling_week,
        loaders=loaders,
    )

    return {
        "current": {
            "closed": utils.format_cvssf(total_current_closed),
            "open": utils.format_cvssf(total_current_open),
        },
        "previous": {
            "closed": utils.format_cvssf(total_previous_closed),
            "open": utils.format_cvssf(total_previous_open),
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
