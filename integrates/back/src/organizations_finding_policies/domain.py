# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .dal import (
    add_organization_finding_policy,
    get_organization_finding_policies,
    get_organization_finding_policy,
    update_finding_policy_status,
)
from aioextensions import (
    collect,
)
from custom_exceptions import (
    FindingNamePolicyNotFound,
    InvalidFindingNamePolicy,
    PolicyAlreadyHandled,
    RepeatedFindingNamePolicy,
)
from dataloaders import (
    Dataloaders,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.findings.types import (
    Finding,
)
from db_model.organization_finding_policies.enums import (
    PolicyStateStatus,
)
from db_model.organization_finding_policies.types import (
    OrgFindingPolicy,
    OrgFindingPolicyRequest,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityTreatment,
)
from dynamodb.types import (
    OrgFindingPolicyItem,
    OrgFindingPolicyMetadata,
    OrgFindingPolicyState,
)
from itertools import (
    chain,
)
from newutils import (
    datetime as datetime_utils,
    findings as findings_utils,
    validations,
    vulnerabilities as vulns_utils,
)
from typing import (
    Optional,
    Union,
)
from uuid import (
    uuid4,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def get_finding_policy(
    *, org_name: str, finding_policy_id: str
) -> OrgFindingPolicyItem:
    finding_policy = await get_organization_finding_policy(
        org_name=org_name, finding_policy_id=finding_policy_id
    )
    if finding_policy:
        return finding_policy

    raise FindingNamePolicyNotFound()


async def get_finding_policies(
    *, org_name: str
) -> tuple[OrgFindingPolicyItem, ...]:
    return await get_organization_finding_policies(org_name=org_name)


async def validate_finding_name(name: str) -> None:
    if not await findings_utils.is_valid_finding_title(name):
        raise InvalidFindingNamePolicy()


async def get_finding_policy_by_name(
    *, org_name: str, finding_name: str
) -> Optional[OrgFindingPolicyItem]:
    return next(
        (
            fin_policy
            for fin_policy in await get_finding_policies(org_name=org_name)
            if fin_policy.metadata.name.lower().endswith(finding_name.lower())
        ),
        None,
    )


async def add_finding_policy(
    *,
    finding_name: str,
    org_name: str,
    tags: Union[set[str], dict],
    user_email: str,
) -> None:
    await validate_finding_name(finding_name)
    finding_policy = await get_finding_policy_by_name(
        org_name=org_name, finding_name=finding_name.lower()
    )
    if finding_policy:
        raise RepeatedFindingNamePolicy()

    validations.validate_fields(tags)
    new_finding_policy = OrgFindingPolicyItem(
        org_name=org_name,
        id=str(uuid4()),
        metadata=OrgFindingPolicyMetadata(name=finding_name, tags=tags),
        state=OrgFindingPolicyState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            status="SUBMITTED",
        ),
    )
    await add_organization_finding_policy(finding_policy=new_finding_policy)


async def handle_finding_policy_acceptance(
    *,
    loaders: Dataloaders,
    finding_policy_id: str,
    modified_by: str,
    organization_name: str,
    status: PolicyStateStatus,
) -> None:
    finding_policy: OrgFindingPolicy = (
        await loaders.organization_finding_policy.load(
            OrgFindingPolicyRequest(
                organization_name=organization_name,
                policy_id=finding_policy_id,
            )
        )
    )
    if finding_policy.state.status != PolicyStateStatus.SUBMITTED:
        raise PolicyAlreadyHandled()

    await update_finding_policy_status(
        org_name=organization_name,
        finding_policy_id=finding_policy_id,
        status=OrgFindingPolicyState(
            modified_by=modified_by,
            modified_date=datetime_utils.get_iso_date(),
            status=status.value,
        ),
    )


async def submit_finding_policy(
    *,
    loaders: Dataloaders,
    finding_policy_id: str,
    modified_by: str,
    organization_name: str,
) -> None:
    finding_policy: OrgFindingPolicy = (
        await loaders.organization_finding_policy.load(
            OrgFindingPolicyRequest(
                organization_name=organization_name,
                policy_id=finding_policy_id,
            )
        )
    )
    if finding_policy.state.status not in {
        PolicyStateStatus.INACTIVE,
        PolicyStateStatus.REJECTED,
    }:
        raise PolicyAlreadyHandled()

    await update_finding_policy_status(
        org_name=organization_name,
        finding_policy_id=finding_policy_id,
        status=OrgFindingPolicyState(
            modified_by=modified_by,
            modified_date=datetime_utils.get_iso_date(),
            status=PolicyStateStatus.SUBMITTED.value,
        ),
    )


async def deactivate_finding_policy(
    *,
    loaders: Dataloaders,
    finding_policy_id: str,
    modified_by: str,
    organization_name: str,
) -> None:
    finding_policy: OrgFindingPolicy = (
        await loaders.organization_finding_policy.load(
            OrgFindingPolicyRequest(
                organization_name=organization_name,
                policy_id=finding_policy_id,
            )
        )
    )
    if finding_policy.state.status != PolicyStateStatus.APPROVED:
        raise PolicyAlreadyHandled()

    await update_finding_policy_status(
        org_name=organization_name,
        finding_policy_id=finding_policy_id,
        status=OrgFindingPolicyState(
            modified_by=modified_by,
            modified_date=datetime_utils.get_iso_date(),
            status=PolicyStateStatus.INACTIVE.value,
        ),
    )


async def update_finding_policy_in_groups(
    *,
    loaders: Dataloaders,
    finding_name: str,
    group_names: list[str],
    status: str,
    user_email: str,
    tags: set[str],
) -> tuple[list[str], list[str]]:
    group_drafts: tuple[
        tuple[Finding, ...], ...
    ] = await loaders.group_drafts.load_many(group_names)
    group_findings: tuple[
        tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(group_names)
    findings = tuple(chain.from_iterable(group_drafts + group_findings))
    findings_ids: list[str] = [
        finding.id
        for finding in findings
        if finding_name.lower().endswith(finding.title.lower())
    ]

    if not findings_ids:
        return [], []
    vulns: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        findings_ids
    )

    await _apply_finding_policy(
        vulns=vulns,
        status=status,
        user_email=user_email,
        tags=tags,
    )
    return findings_ids, [vuln.id for vuln in vulns]


async def _apply_finding_policy(
    vulns: tuple[Vulnerability, ...],
    status: str,
    user_email: str,
    tags: set[str],
) -> None:
    current_day: str = datetime_utils.get_iso_date()
    if status not in {"APPROVED", "INACTIVE"}:
        return
    if status == "APPROVED":
        await collect(
            (
                _add_accepted_treatment(
                    current_day=current_day,
                    vulns=vulns,
                    user_email=user_email,
                ),
                _add_tags_to_vulnerabilities(
                    vulns=vulns,
                    tags=tags,
                ),
            )
        )
    if status == "INACTIVE":
        await _add_new_treatment(
            current_day=current_day,
            vulns=vulns,
            user_email=user_email,
        )


async def _add_accepted_treatment(
    *,
    current_day: str,
    vulns: tuple[Vulnerability, ...],
    user_email: str,
) -> None:
    vulns_to_update = [
        vuln
        for vuln in vulns
        if vuln.treatment is not None
        if vuln.treatment.status
        != VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        and vuln.state.status == VulnerabilityStateStatus.OPEN
    ]
    (  # pylint: disable=unbalanced-tuple-unpacking
        acceptance_submitted,
        acceptance_approved,
    ) = vulns_utils.get_treatment_from_org_finding_policy(
        modified_date=current_day, user_email=user_email
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
    vulns: tuple[Vulnerability, ...],
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
    current_day: str,
    vulns: tuple[Vulnerability, ...],
    user_email: str,
) -> None:
    vulns_to_update = [
        vuln
        for vuln in vulns
        if vuln.treatment is not None
        if vuln.treatment.status != VulnerabilityTreatmentStatus.NEW
    ]
    await collect(
        [
            vulns_model.update_treatment(
                current_value=vuln,
                finding_id=vuln.finding_id,
                vulnerability_id=vuln.id,
                treatment=VulnerabilityTreatment(
                    modified_date=current_day,
                    status=VulnerabilityTreatmentStatus.NEW,
                    modified_by=user_email,
                ),
            )
            for vuln in vulns_to_update
        ],
        workers=20,
    )
