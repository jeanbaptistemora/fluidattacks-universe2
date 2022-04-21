from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityTreatmentStatus,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    datetime as datetime_utils,
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


async def reset_group_expired_accepted_findings(
    loaders: Dataloaders, group_name: str, today: datetime
) -> None:
    group_findings: tuple[Finding] = await loaders.group_findings.load(
        group_name
    )
    vulns = await loaders.finding_vulnerabilities.load_many_chained(
        [finding.id for finding in group_findings]
    )
    updated_finding_ids: set[str] = set()
    updated_vuln_ids: set[str] = set()

    for vuln in vulns:
        finding_id = vuln.finding_id
        is_accepted_expired = (
            datetime.fromisoformat(vuln.treatment.accepted_until) < today
            if vuln.treatment and vuln.treatment.accepted_until
            else False
        )
        is_undefined_accepted_expired = (
            vuln.treatment
            and vuln.treatment.status
            == VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
            and vuln.treatment.acceptance_status
            == VulnerabilityAcceptanceStatus.SUBMITTED
            and datetime_utils.get_plus_delta(
                datetime.fromisoformat(vuln.treatment.modified_date),
                days=5,
            )
            <= today
        )
        if is_accepted_expired or is_undefined_accepted_expired:
            updated_values = {"treatment": "NEW"}
            await vulns_domain.add_vulnerability_treatment(
                finding_id=finding_id,
                updated_values=updated_values,
                vuln=vuln,
                user_email=vuln.treatment.modified_by,
            )
            updated_finding_ids.add(finding_id)
            updated_vuln_ids.add(vuln.id)

    await update_unreliable_indicators_by_deps(
        EntityDependency.reset_expired_accepted_findings,
        finding_ids=updated_finding_ids,
        vulnerability_ids=updated_vuln_ids,
    )


async def reset_expired_accepted_findings() -> None:
    """Update treatment if acceptance date expires."""
    today: datetime = datetime_utils.get_now()
    loaders: Dataloaders = get_new_context()
    groups = await groups_domain.get_active_groups()
    await collect(
        [
            reset_group_expired_accepted_findings(loaders, group_name, today)
            for group_name in groups
        ],
        workers=40,
    )


async def main() -> None:
    await reset_expired_accepted_findings()
