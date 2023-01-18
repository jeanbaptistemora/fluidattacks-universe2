from aioextensions import (
    collect,
)
from botocore.exceptions import (
    ConnectTimeoutError,
    ReadTimeoutError,
)
from custom_exceptions import (
    UnavailabilityError as CustomUnavailabilityError,
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
from dynamodb.exceptions import (
    UnavailabilityError,
)
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    domain as orgs_domain,
)
from schedulers.common import (
    info,
)
from typing import (
    Optional,
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
from vulnerabilities.types import (
    VulnerabilityTreatmentToUpdate,
)


@retry_on_exceptions(
    exceptions=(
        CustomUnavailabilityError,
        UnavailabilityError,
        VulnNotFound,
    ),
)
async def process_vulnerability(
    vulnerability: Vulnerability,
) -> Optional[str]:
    today = datetime_utils.get_utc_now()
    is_accepted_expired = (
        vulnerability.treatment.accepted_until < today
        if vulnerability.treatment and vulnerability.treatment.accepted_until
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
        await vulns_domain.add_vulnerability_treatment(
            modified_by=vulnerability.treatment.modified_by,
            treatment=VulnerabilityTreatmentToUpdate(
                accepted_until=None,
                assigned=None,
                justification="Expired accepted treatment",
                status=VulnerabilityTreatmentStatus.UNTREATED,
            ),
            vulnerability=vulnerability,
        )
        return vulnerability.id

    return None


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
)
async def process_finding(loaders: Dataloaders, finding: Finding) -> None:
    vulnerabilities = await loaders.finding_vulnerabilities.load(finding.id)
    results = await collect(
        tuple(
            process_vulnerability(vulnerability)
            for vulnerability in vulnerabilities
        ),
        workers=4,
    )
    updated_vulnerability_ids = [id for id in results if id]
    if not updated_vulnerability_ids:
        return

    await update_unreliable_indicators_by_deps(
        EntityDependency.reset_expired_accepted_findings,
        finding_ids=[finding.id],
        vulnerability_ids=list(updated_vulnerability_ids),
    )
    info(
        "Finding processed",
        extra={
            "finding_id": finding.id,
            "finding_title": finding.title,
            "group_name": finding.group_name,
            "updated_vulnerability_ids": updated_vulnerability_ids,
        },
    )


@retry_on_exceptions(
    exceptions=(ReadTimeoutError, ConnectTimeoutError),
)
async def process_group(
    loaders: Dataloaders, group_name: str, progress: float
) -> None:
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    await collect(
        tuple(process_finding(loaders, finding) for finding in group_findings),
        workers=4,
    )
    info(
        "Group processed",
        extra={
            "name": group_name,
            "findings": len(group_findings),
            "progress": round(progress, 2),
        },
    )


async def reset_expired_accepted_findings() -> None:
    """Update treatment if acceptance date expires."""
    loaders: Dataloaders = get_new_context()
    group_names = sorted(await orgs_domain.get_all_active_group_names(loaders))
    info("Groups to process", extra={"item": len(group_names)})
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / len(group_names),
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=1,
    )


async def main() -> None:
    await reset_expired_accepted_findings()
