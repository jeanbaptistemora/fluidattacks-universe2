from aioextensions import (
    collect,
)
from custom_exceptions import (
    VulnNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    retry_on_exceptions,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerabilities import (
    domain as vulns_domain,
)


@retry_on_exceptions(exceptions=(VulnNotFound,), sleep_seconds=2.0)
async def _reset_expired_accepted_vuln(
    loaders: Dataloaders, vuln_id: str
) -> None:
    updated_values = {"treatment": "UNTREATED"}
    loaders.vulnerability.clear(vuln_id)
    vuln_to_update: Vulnerability = await loaders.vulnerability.load(vuln_id)
    if vuln_to_update.treatment and vuln_to_update.treatment.modified_by:
        await vulns_domain.add_vulnerability_treatment(
            finding_id=vuln_to_update.finding_id,
            updated_values=updated_values,
            vuln=vuln_to_update,
            user_email=vuln_to_update.treatment.modified_by,
        )


async def _process_finding(loaders: Dataloaders, finding_id: str) -> None:
    today = datetime_utils.get_utc_now()
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load(finding_id)
    updated_vuln_ids: set[str] = set()

    for vulnerability in vulnerabilities:
        is_accepted_expired = (
            vulnerability.treatment.accepted_until < today
            if vulnerability.treatment
            and vulnerability.treatment.accepted_until
            else False
        )
        is_undefined_accepted_expired = (
            vulnerability.treatment
            and vulnerability.treatment.status
            == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
            and vulnerability.treatment.acceptance_status
            == VulnerabilityAcceptanceStatus.SUBMITTED
            and datetime_utils.get_plus_delta(
                vulnerability.treatment.modified_date,
                days=5,
            )
            <= today
        )
        if (
            vulnerability.treatment
            and vulnerability.treatment.modified_by
            and (is_accepted_expired or is_undefined_accepted_expired)
        ):
            await _reset_expired_accepted_vuln(loaders, vulnerability.id)
            updated_vuln_ids.add(vulnerability.id)

    if updated_vuln_ids:
        await update_unreliable_indicators_by_deps(
            EntityDependency.reset_expired_accepted_findings,
            finding_ids=[finding_id],
            vulnerability_ids=list(updated_vuln_ids),
        )


async def _process_group(loaders: Dataloaders, group_name: str) -> None:
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    await collect(
        tuple(
            _process_finding(loaders, finding_id)
            for finding_id in tuple(finding.id for finding in group_findings)
        ),
        workers=4,
    )


async def reset_expired_accepted_findings() -> None:
    """Update treatment if acceptance date expires."""
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)
    await collect(
        tuple(
            _process_group(loaders, group_name) for group_name in group_names
        ),
        workers=4,
    )


async def main() -> None:
    await reset_expired_accepted_findings()
