from aioextensions import (
    collect,
)
from custom_exceptions import (
    InvalidFindingNamePolicy,
    OrgFindingPolicyNotFound,
    PolicyAlreadyHandled,
    RepeatedFindingNamePolicy,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
)
from db_model import (
    organization_finding_policies as polices_model,
    vulnerabilities as vulns_model,
)
from db_model.organization_finding_policies.enums import (
    PolicyStateStatus,
)
from db_model.organization_finding_policies.types import (
    OrgFindingPolicy,
    OrgFindingPolicyRequest,
    OrgFindingPolicyState,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
    validations,
    vulnerabilities as vulns_utils,
)
from uuid import (
    uuid4,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def validate_finding_name(loaders: Dataloaders, name: str) -> None:
    if not await findings_utils.is_valid_finding_title(loaders, name):
        raise InvalidFindingNamePolicy()


async def get_finding_policy_by_name(
    *,
    loaders: Dataloaders,
    finding_name: str,
    organization_name: str,
) -> OrgFindingPolicy | None:
    org_finding_policies = await loaders.organization_finding_policies.load(
        organization_name
    )

    return next(
        (
            finding_policy
            for finding_policy in org_finding_policies
            if finding_policy.name.lower().endswith(finding_name.lower())
        ),
        None,
    )


@validations.validate_fields_deco(["tags"])
async def add_finding_policy(
    *,
    loaders: Dataloaders,
    email: str,
    finding_name: str,
    organization_name: str,
    tags: set[str],
) -> None:
    await validate_finding_name(loaders, finding_name)
    finding_policy = await get_finding_policy_by_name(
        loaders=loaders,
        organization_name=organization_name,
        finding_name=finding_name.lower(),
    )
    if finding_policy:
        raise RepeatedFindingNamePolicy()

    await polices_model.add(
        policy=OrgFindingPolicy(
            id=str(uuid4()),
            organization_name=organization_name,
            name=finding_name,
            state=OrgFindingPolicyState(
                modified_by=email,
                modified_date=datetime_utils.get_utc_now(),
                status=PolicyStateStatus.SUBMITTED,
            ),
            tags=tags,
        )
    )


async def handle_finding_policy_acceptance(
    *,
    loaders: Dataloaders,
    email: str,
    finding_policy_id: str,
    organization_name: str,
    status: PolicyStateStatus,
) -> None:
    finding_policy: (
        OrgFindingPolicy | None
    ) = await loaders.organization_finding_policy.load(
        OrgFindingPolicyRequest(
            organization_name=organization_name,
            policy_id=finding_policy_id,
        )
    )
    if not finding_policy:
        raise OrgFindingPolicyNotFound()
    if finding_policy.state.status != PolicyStateStatus.SUBMITTED:
        raise PolicyAlreadyHandled()

    await polices_model.update(
        organization_name=organization_name,
        finding_policy_id=finding_policy_id,
        state=OrgFindingPolicyState(
            modified_by=email,
            modified_date=datetime_utils.get_utc_now(),
            status=status,
        ),
    )


async def submit_finding_policy(
    *,
    loaders: Dataloaders,
    email: str,
    finding_policy_id: str,
    organization_name: str,
) -> None:
    finding_policy: (
        OrgFindingPolicy | None
    ) = await loaders.organization_finding_policy.load(
        OrgFindingPolicyRequest(
            organization_name=organization_name,
            policy_id=finding_policy_id,
        )
    )
    if not finding_policy:
        raise OrgFindingPolicyNotFound()
    if finding_policy.state.status not in {
        PolicyStateStatus.INACTIVE,
        PolicyStateStatus.REJECTED,
    }:
        raise PolicyAlreadyHandled()

    await polices_model.update(
        organization_name=organization_name,
        finding_policy_id=finding_policy_id,
        state=OrgFindingPolicyState(
            modified_by=email,
            modified_date=datetime_utils.get_utc_now(),
            status=PolicyStateStatus.SUBMITTED,
        ),
    )


async def deactivate_finding_policy(
    *,
    loaders: Dataloaders,
    email: str,
    finding_policy_id: str,
    organization_name: str,
) -> None:
    finding_policy: (
        OrgFindingPolicy | None
    ) = await loaders.organization_finding_policy.load(
        OrgFindingPolicyRequest(
            organization_name=organization_name,
            policy_id=finding_policy_id,
        )
    )
    if not finding_policy:
        raise OrgFindingPolicyNotFound()
    if finding_policy.state.status != PolicyStateStatus.APPROVED:
        raise PolicyAlreadyHandled()

    await polices_model.update(
        organization_name=organization_name,
        finding_policy_id=finding_policy_id,
        state=OrgFindingPolicyState(
            modified_by=email,
            modified_date=datetime_utils.get_utc_now(),
            status=PolicyStateStatus.INACTIVE,
        ),
    )


async def update_finding_policy_in_groups(
    *,
    loaders: Dataloaders,
    email: str,
    finding_name: str,
    group_names: list[str],
    status: PolicyStateStatus,
    tags: set[str],
) -> tuple[list[str], list[str]]:
    findings = await loaders.group_drafts_and_findings.load_many_chained(
        group_names
    )
    findings_ids: list[str] = [
        finding.id
        for finding in findings
        if finding_name.lower().endswith(finding.title.lower())
    ]

    if not findings_ids:
        return [], []
    vulns = (
        await loaders.finding_vulnerabilities_released_nzr.load_many_chained(
            findings_ids
        )
    )

    await _apply_finding_policy(
        vulns=vulns,
        status=status,
        email=email,
        tags=tags,
    )
    return findings_ids, [vuln.id for vuln in vulns]


async def _apply_finding_policy(
    vulns: list[Vulnerability],
    status: PolicyStateStatus,
    email: str,
    tags: set[str],
) -> None:
    modified_date = datetime_utils.get_utc_now()
    if status not in {PolicyStateStatus.APPROVED, PolicyStateStatus.INACTIVE}:
        return
    if status == PolicyStateStatus.APPROVED:
        await collect(
            (
                _add_accepted_treatment(
                    modified_date=modified_date,
                    vulns=vulns,
                    email=email,
                ),
                _add_tags_to_vulnerabilities(
                    vulns=vulns,
                    tags=tags,
                ),
            )
        )
    elif status == PolicyStateStatus.INACTIVE:
        await _add_new_treatment(
            modified_date=modified_date,
            vulns=vulns,
            email=email,
        )


async def _add_accepted_treatment(
    *,
    modified_date: datetime,
    vulns: list[Vulnerability],
    email: str,
) -> None:
    vulns_to_update = [
        vuln
        for vuln in vulns
        if vuln.treatment is not None
        if vuln.treatment.status
        != VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        and vuln.state.status == VulnerabilityStateStatus.VULNERABLE
    ]
    (  # pylint: disable=unbalanced-tuple-unpacking
        acceptance_submitted,
        acceptance_approved,
    ) = vulns_utils.get_treatment_from_org_finding_policy(
        modified_date=modified_date, user_email=email
    )
    await collect(
        [
            vulns_model.update_treatment(
                current_value=vuln,
                finding_id=vuln.finding_id,
                vulnerability_id=vuln.id,
                treatment=acceptance_submitted,
            )
            for vuln in vulns_to_update
        ],
        workers=20,
    )
    await collect(
        [
            vulns_model.update_treatment(
                current_value=vuln._replace(treatment=acceptance_submitted),
                finding_id=vuln.finding_id,
                vulnerability_id=vuln.id,
                treatment=acceptance_approved,
            )
            for vuln in vulns_to_update
        ],
        workers=20,
    )


async def _add_tags_to_vulnerabilities(
    *,
    vulns: list[Vulnerability],
    tags: set[str],
) -> None:
    if not tags:
        return
    await collect(
        [
            vulns_domain.add_tags(vulnerability=vuln, tags=list(tags))
            for vuln in vulns
        ],
        workers=20,
    )


async def _add_new_treatment(
    *,
    modified_date: datetime,
    vulns: list[Vulnerability],
    email: str,
) -> None:
    vulns_to_update = [
        vuln
        for vuln in vulns
        if vuln.treatment is not None
        if vuln.treatment.status != VulnerabilityTreatmentStatus.UNTREATED
    ]
    await collect(
        [
            vulns_model.update_treatment(
                current_value=vuln,
                finding_id=vuln.finding_id,
                vulnerability_id=vuln.id,
                treatment=VulnerabilityTreatment(
                    modified_date=modified_date,
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                    modified_by=email,
                ),
            )
            for vuln in vulns_to_update
        ],
        workers=20,
    )
