from .dal import (
    add_organization_finding_policy,
    get_organization_finding_policies,
    get_organization_finding_policy,
    update_finding_policy_status,
)
from .types import (
    OrgFindingPolicy,
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
from db_model.findings.types import (
    Finding,
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
from redis_cluster.operations import (
    redis_del_by_deps,
)
from typing import (
    Any,
    List,
    Optional,
    Set,
    Tuple,
)
from uuid import (
    uuid4,
)
from vulnerabilities import (
    dal as vulns_dal,
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
) -> Tuple[OrgFindingPolicyItem, ...]:
    return await get_organization_finding_policies(org_name=org_name)


def validate_finding_name(name: str) -> None:
    if not findings_utils.is_valid_finding_title(name):
        raise InvalidFindingNamePolicy()


async def get_finding_policy_by_name(
    *, org_name: str, finding_name: str
) -> Optional[OrgFindingPolicyItem]:
    return next(
        (
            fin_policy
            for fin_policy in await get_finding_policies(org_name=org_name)
            if fin_policy.metadata.name.split(".")[0]
            .lower()
            .endswith(finding_name)
        ),
        None,
    )


async def add_finding_policy(
    *,
    finding_name: str,
    org_name: str,
    tags: Set[str],
    user_email: str,
) -> None:
    validate_finding_name(finding_name)
    finding_policy = await get_finding_policy_by_name(
        org_name=org_name,
        finding_name=finding_name.split(".")[0].lower(),
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
    finding_policy_id: str,
    org_name: str,
    status: str,
    user_email: str,
) -> None:
    finding_policy = await get_finding_policy(
        org_name=org_name, finding_policy_id=finding_policy_id
    )
    if finding_policy.state.status != "SUBMITTED":
        raise PolicyAlreadyHandled()

    await update_finding_policy_status(
        org_name=org_name,
        finding_policy_id=finding_policy_id,
        status=OrgFindingPolicyState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            status=status,
        ),
    )


async def submit_finding_policy(
    *,
    finding_policy_id: str,
    organization_name: str,
    user_email: str,
) -> None:
    finding_policy = await get_finding_policy(
        org_name=organization_name, finding_policy_id=finding_policy_id
    )
    status: str = finding_policy.state.status
    is_status_valid: bool = status in {"INACTIVE", "REJECTED"}
    if not is_status_valid:
        raise PolicyAlreadyHandled()

    await update_finding_policy_status(
        org_name=organization_name,
        finding_policy_id=finding_policy_id,
        status=OrgFindingPolicyState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            status="SUBMITTED",
        ),
    )


async def deactivate_finding_policy(
    *,
    finding_policy_id: str,
    org_name: str,
    user_email: str,
) -> None:
    finding_policy = await get_finding_policy(
        org_name=org_name, finding_policy_id=finding_policy_id
    )
    if finding_policy.state.status != "APPROVED":
        raise PolicyAlreadyHandled()

    status: str = "INACTIVE"
    await update_finding_policy_status(
        org_name=org_name,
        finding_policy_id=finding_policy_id,
        status=OrgFindingPolicyState(
            modified_by=user_email,
            modified_date=datetime_utils.get_iso_date(),
            status=status,
        ),
    )


async def update_finding_policy_in_groups(
    *,
    finding_name: str,
    loaders: Any,
    groups: List[str],
    status: str,
    user_email: str,
    tags: Set[str],
) -> None:
    group_drafts: Tuple[
        Tuple[Finding, ...], ...
    ] = await loaders.group_drafts.load_many(groups)
    group_findings: Tuple[
        Tuple[Finding, ...], ...
    ] = await loaders.group_findings.load_many(groups)
    findings = tuple(chain.from_iterable(group_drafts + group_findings))
    findings_ids: List[str] = [
        finding.id
        for finding in findings
        if finding_name.lower().endswith(finding.title.split(".")[0].lower())
    ]

    if not findings_ids:
        return
    vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulns_nzr_typed.load_many_chained(findings_ids)

    await _apply_finding_policy(
        findings_ids=findings_ids,
        vulns=vulns,
        status=status,
        user_email=user_email,
        tags=tags,
    )


async def _apply_finding_policy(
    findings_ids: List[str],
    vulns: Tuple[Vulnerability, ...],
    status: str,
    user_email: str,
    tags: Set[str],
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

    await collect(
        [
            redis_del_by_deps(
                "update_vulnerability_treatment", finding_id=finding_id
            )
            for finding_id in findings_ids
        ],
        workers=20,
    )


async def _add_accepted_treatment(
    *,
    current_day: str,
    vulns: Tuple[Vulnerability, ...],
    user_email: str,
) -> None:
    vulns_to_update = [
        vuln
        for vuln in vulns
        if vuln.treatment.status
        != VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        and vuln.state.status == VulnerabilityStateStatus.OPEN
    ]
    (
        acceptance_submitted,
        acceptance_approved,
    ) = vulns_utils.get_treatment_from_org_finding_policy(
        modified_date=current_day, user_email=user_email
    )
    await collect(
        [
            vulns_dal.update_treatment(
                current_value=vuln.treatment,
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
            vulns_dal.update_treatment(
                current_value=vuln.treatment,
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
    vulns: Tuple[Vulnerability, ...],
    tags: Set[str],
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
    vulns: Tuple[Vulnerability, ...],
    user_email: str,
) -> None:
    vulns_to_update = [
        vuln
        for vuln in vulns
        if vuln.treatment.status != VulnerabilityTreatmentStatus.NEW
    ]
    await collect(
        [
            vulns_dal.update_treatment(
                current_value=vuln.treatment,
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


async def get_org_policies(*, org_name: str) -> Tuple[OrgFindingPolicy, ...]:
    finding_policies = await get_organization_finding_policies(
        org_name=org_name
    )
    return tuple(
        OrgFindingPolicy(
            id=policy.id,
            last_status_update=policy.state.modified_date,
            name=policy.metadata.name,
            status=policy.state.status,
            tags=policy.metadata.tags,
        )
        for policy in finding_policies
    )
