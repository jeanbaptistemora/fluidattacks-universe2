# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint:disable=too-many-lines

from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    schedule,
)
import authz
from authz.validations import (
    validate_role_fluid_reqs,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
    Product,
)
from batch.types import (
    BatchProcessing,
)
import bugsnag
from collections import (
    Counter,
)
from context import (
    BASE_URL,
    FI_ENVIRONMENT,
)
from custom_exceptions import (
    AlreadyPendingDeletion,
    BillingSubscriptionSameActive,
    ErrorUpdatingGroup,
    GroupHasPendingActions,
    GroupNotFound,
    InvalidAcceptanceSeverityRange,
    InvalidGroupName,
    InvalidGroupServicesConfig,
    InvalidGroupTier,
    InvalidManagedChange,
    InvalidParameter,
    RepeatedValues,
    StakeholderNotInOrganization,
    TrialRestriction,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    date,
    datetime,
)
from db_model import (
    enrollment as enrollment_model,
    forces as forces_model,
    groups as groups_model,
    toe_inputs as toe_inputs_model,
    toe_lines as toe_lines_model,
)
from db_model.constants import (
    POLICIES_FORMATTED,
)
from db_model.enrollment.types import (
    Enrollment,
    Trial,
)
from db_model.enums import (
    Notification,
)
from db_model.events.types import (
    Event,
    GroupEventsRequest,
)
from db_model.findings.types import (
    Finding,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
    GroupAccessState,
    GroupInvitation,
)
from db_model.groups.constants import (
    MASKED,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupStateUpdationJustification,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupFile,
    GroupMetadataToUpdate,
    GroupState,
    GroupStatusJustification,
    GroupTreatmentSummary,
    GroupUnreliableIndicators,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderMetadataToUpdate,
)
from db_model.types import (
    PoliciesToUpdate,
)
from db_model.utils import (
    get_min_iso_date,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from enrollment import (
    domain as enrollment_domain,
)
from events import (
    domain as events_domain,
)
from findings import (
    domain as findings_domain,
)
from group_access import (
    domain as group_access_domain,
)
from group_comments import (
    domain as group_comments_domain,
)
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
    groups as groups_utils,
    resources as resources_utils,
    validations,
    vulnerabilities as vulns_utils,
)
from newutils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
    validate_fields,
    validate_group_name,
    validate_string_length_between,
)
from notifications import (
    domain as notifications_domain,
)
from organizations import (
    domain as orgs_domain,
)
import re
from roots import (
    domain as roots_domain,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from typing import (
    Any,
    Awaitable,
    Optional,
)


async def _has_repeated_tags(
    loaders: Dataloaders, group_name: str, tags: list[str]
) -> bool:
    has_repeated_tags = len(tags) != len(set(tags))
    if not has_repeated_tags:
        group: Group = await loaders.group.load(group_name)
        existing_tags = group.state.tags
        all_tags = list(existing_tags or {}) + tags
        has_repeated_tags = len(all_tags) != len(set(all_tags))
    return has_repeated_tags


async def complete_register_for_group_invitation(
    loaders: Dataloaders,
    group_access: GroupAccess,
) -> None:
    invitation = group_access.invitation
    if invitation and invitation.is_used:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    group_name = group_access.group_name
    email = group_access.email
    if invitation:
        responsibility = invitation.responsibility
        role = invitation.role
        url_token = invitation.url_token

    coroutines: list[Awaitable[None]] = []
    coroutines.append(
        authz.grant_group_level_role(loaders, email, group_name, role)
    )
    group: Group = await loaders.group.load(group_name)
    organization_id = group.organization_id
    if not await orgs_domain.has_access(loaders, organization_id, email):
        coroutines.append(
            orgs_domain.add_stakeholder(
                loaders, organization_id, email, "user"
            )
        )
    coroutines.append(
        group_access_domain.update(
            loaders=loaders,
            email=email,
            group_name=group_name,
            metadata=GroupAccessMetadataToUpdate(
                expiration_time=0,
                has_access=True,
                invitation=GroupInvitation(
                    is_used=True,
                    role=role,
                    url_token=url_token,
                    responsibility=responsibility,
                ),
                responsibility=responsibility,
                state=GroupAccessState(
                    modified_date=datetime_utils.get_iso_date()
                ),
            ),
        )
    )
    if await stakeholders_domain.exists(loaders, email):
        stakeholder: Stakeholder = await loaders.stakeholder.load(email)
        if not stakeholder.is_registered:
            coroutines.extend(
                [
                    stakeholders_domain.register(email),
                    authz.grant_user_level_role(email, "user"),
                ]
            )
    else:
        coroutines.append(
            stakeholders_domain.update(
                email=email, metadata=StakeholderMetadataToUpdate()
            )
        )
    enrollment: Enrollment = await loaders.enrollment.load(email)
    if not enrollment.enrolled:
        coroutines.append(
            enrollment_model.add(
                enrollment=Enrollment(
                    email=email,
                    enrolled=True,
                    trial=Trial(
                        completed=True,
                        extension_date="",
                        extension_days=0,
                        start_date="",
                    ),
                )
            )
        )

    await collect(coroutines)


async def reject_register_for_group_invitation(
    loaders: Dataloaders,
    group_access: GroupAccess,
) -> None:
    invitation = group_access.invitation
    if invitation and invitation.is_used:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    await group_access_domain.remove_access(
        loaders=loaders,
        email=group_access.email,
        group_name=group_access.group_name,
    )


async def add_group(
    *,
    loaders: Dataloaders,
    description: str,
    email: str,
    granted_role: str,
    group_name: str,
    organization_name: str,
    service: GroupService,
    has_machine: bool = False,
    has_squad: bool = False,
    language: GroupLanguage = GroupLanguage.EN,
    subscription: GroupSubscriptionType = GroupSubscriptionType.CONTINUOUS,
    tier: GroupTier = GroupTier.FREE,
) -> None:
    validate_group_name(group_name)
    validate_fields([description])
    validate_field_length(group_name, 20)
    validate_field_length(description, 200)
    validate_group_services_config(
        has_machine,
        has_squad,
        has_arm=True,
    )

    if not description.strip() or not group_name.strip():
        raise InvalidParameter()

    organization: Organization = await loaders.organization.load(
        organization_name
    )
    if not await orgs_domain.has_access(loaders, organization.id, email):
        raise StakeholderNotInOrganization(organization.id)

    if await exists(loaders, group_name):
        raise InvalidGroupName.new()

    if await enrollment_domain.is_trial(loaders, email, organization):
        managed = GroupManaged.TRIAL
        if (
            await loaders.organization_groups.load(organization.id)
            or has_squad
            or not has_machine
            or service != GroupService.WHITE
            or subscription != GroupSubscriptionType.CONTINUOUS
        ):
            raise TrialRestriction()
    else:
        managed = GroupManaged.MANAGED

    await groups_model.add(
        group=Group(
            created_by=email,
            created_date=datetime_utils.get_iso_date(),
            description=description,
            language=language,
            name=group_name,
            state=GroupState(
                has_machine=has_machine,
                has_squad=has_squad,
                managed=managed,
                modified_by=email,
                modified_date=datetime_utils.get_iso_date(),
                service=service,
                status=GroupStateStatus.ACTIVE,
                tier=tier,
                type=subscription,
            ),
            organization_id=organization.id,
            sprint_duration=1,
            sprint_start_date=get_min_iso_date(
                datetime.fromisoformat(datetime_utils.get_iso_date())
            ).isoformat(),
        )
    )
    await orgs_domain.add_group_access(loaders, organization.id, group_name)

    # Admins are not granted access to the group
    # they are omnipresent
    if granted_role != "admin":
        await group_access_domain.update(
            loaders=loaders,
            email=email,
            group_name=group_name,
            metadata=GroupAccessMetadataToUpdate(
                has_access=True,
                state=GroupAccessState(
                    modified_date=datetime_utils.get_iso_date()
                ),
            ),
        )
        # Only Fluid staff can be customer managers
        # Customers are granted the user manager role
        role: str = (
            "customer_manager"
            if stakeholders_domain.is_fluid_staff(email)
            else "user_manager"
        )
        await authz.grant_group_level_role(loaders, email, group_name, role)

    # Notify us in case the stakeholder wants any Fluid Service
    await notifications_domain.new_group(
        description=description,
        group_name=group_name,
        has_machine=has_machine,
        has_squad=has_squad,
        organization=organization_name,
        requester_email=email,
        service=service,
        subscription=subscription,
    )


async def deactivate_all_roots(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
    other: str = "",
    reason: str = "",
) -> None:
    group_roots_loader: DataLoader = loaders.group_roots
    all_group_roots = await group_roots_loader.load(group_name)
    await collect(
        [
            roots_domain.deactivate_root(
                group_name=group_name,
                other=other,
                reason=reason,
                root=root,
                email=email,
            )
            for root in all_group_roots
        ]
    )


async def remove_group(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
    justification: GroupStatusJustification,
    validate_pending_actions: bool = True,
) -> None:
    """
    Update group state to DELETED and update some related resources.
    For production, remember to remove additional resources
    (stakeholder, findings, vulns ,etc) via the batch action
    remove_group_resources.
    """
    loaders.group.clear(group_name)
    group: Group = await loaders.group.load(group_name)
    if group.state.status == GroupStateStatus.DELETED:
        raise AlreadyPendingDeletion()

    if validate_pending_actions:
        cancelable_actions = {
            Action.EXECUTE_MACHINE.value,
            Action.REFRESH_TOE_INPUTS.value,
            Action.REFRESH_TOE_LINES.value,
            Action.CLONE_ROOTS.value,
        }
        group_actions: list[BatchProcessing] = [
            action
            for action in await batch_dal.get_actions()
            if action.entity == group_name
        ]
        pending_actions = [
            action
            for action in group_actions
            if action.action_name not in cancelable_actions
        ]
        actions_to_delete = [
            action
            for action in group_actions
            if action.action_name in cancelable_actions
        ]
        if pending_actions:
            raise GroupHasPendingActions()

        await collect(
            [
                batch_dal.delete_action(dynamodb_pk=action.key)
                for action in actions_to_delete
            ]
        )
        await collect(
            [
                batch_dal.cancel_batch_job(job_id=action.batch_job_id)
                for action in actions_to_delete
                if action.batch_job_id
            ]
        )

    await remove_all_stakeholders(
        loaders=loaders,
        group_name=group_name,
        modified_by=email,
    )
    await groups_model.update_state(
        group_name=group_name,
        organization_id=group.organization_id,
        state=group.state._replace(
            modified_date=datetime_utils.get_iso_date(),
            has_machine=False,
            has_squad=False,
            justification=justification,
            modified_by=email,
            status=GroupStateStatus.DELETED,
        ),
    )

    await batch_dal.put_action(
        action=Action.REMOVE_GROUP_RESOURCES,
        entity=group_name,
        subject=email,
        additional_info="remove_group",
        queue="small",
        product_name=Product.INTEGRATES,
    )
    if FI_ENVIRONMENT == "development":
        await remove_resources(
            loaders=loaders,
            group_name=group_name,
            email=email,
        )


async def update_group_managed(
    *,
    loaders: Dataloaders,
    comments: str,
    email: str,
    group_name: str,
    managed: GroupManaged,
) -> None:
    validate_fields([comments])
    validate_string_length_between(comments, 0, 250)
    group: Group = await loaders.group.load(group_name)

    if managed != group.state.managed:
        if (
            managed == GroupManaged.MANAGED
            and group.state.managed == GroupManaged.UNDER_REVIEW
        ) or (
            managed == GroupManaged.UNDER_REVIEW
            and group.state.managed
            in {GroupManaged.MANAGED, GroupManaged.TRIAL}
        ):
            await update_state(
                group_name=group_name,
                organization_id=group.organization_id,
                state=GroupState(
                    comments=comments,
                    modified_date=datetime_utils.get_iso_date(),
                    has_machine=group.state.has_machine,
                    has_squad=group.state.has_squad,
                    managed=managed,
                    payment_id=group.state.payment_id,
                    justification=GroupStateUpdationJustification["NONE"],
                    modified_by=email,
                    service=group.state.service,
                    status=GroupStateStatus.ACTIVE,
                    tags=group.state.tags,
                    tier=group.state.tier,
                    type=group.state.type,
                ),
            )
        else:
            raise InvalidManagedChange()

        if managed == "MANAGED":
            organization: Organization = await loaders.organization.load(
                group.organization_id
            )
            await notifications_domain.request_managed(
                group_name=group_name,
                managed=managed,
                organization_name=organization.name,
                requester_email=email,
            )


async def update_group_payment_id(
    *,
    group: Group,
    comments: str,
    email: str,
    group_name: str,
    payment_id: str,
    managed: GroupManaged,
) -> None:
    validate_fields([comments])
    validate_string_length_between(comments, 0, 250)
    if payment_id != group.state.payment_id:
        await update_state(
            group_name=group_name,
            organization_id=group.organization_id,
            state=GroupState(
                comments=comments,
                modified_date=datetime_utils.get_iso_date(),
                has_machine=group.state.has_machine,
                has_squad=group.state.has_squad,
                managed=managed,
                justification=GroupStateUpdationJustification["NONE"],
                modified_by=email,
                payment_id=payment_id,
                service=group.state.service,
                status=GroupStateStatus.ACTIVE,
                tags=group.state.tags,
                tier=group.state.tier,
                type=group.state.type,
            ),
        )


async def update_group(
    *,
    loaders: Dataloaders,
    comments: str,
    email: str,
    group_name: str,
    has_arm: bool,
    has_machine: bool,
    has_squad: bool,
    justification: GroupStatusJustification,
    service: Optional[GroupService],
    subscription: GroupSubscriptionType,
    tier: GroupTier = GroupTier.OTHER,
) -> None:
    validate_fields([comments])
    validate_string_length_between(comments, 0, 250)
    validate_group_services_config(
        has_machine,
        has_squad,
        has_arm,
    )

    group: Group = await loaders.group.load(group_name)
    organization: Organization = await loaders.organization.load(
        group.organization_id
    )
    if await enrollment_domain.is_trial(loaders, email, organization) and (
        has_squad
        or not has_machine
        or service != GroupService.WHITE
        or subscription != GroupSubscriptionType.CONTINUOUS
    ):
        raise TrialRestriction()

    if service != group.state.service:
        await deactivate_all_roots(
            loaders=loaders,
            email=email,
            group_name=group_name,
            other=comments,
            reason=justification.value,
        )
    if tier == GroupTier.OTHER:
        tier = GroupTier.FREE

    await update_state(
        group_name=group_name,
        organization_id=group.organization_id,
        state=GroupState(
            comments=comments,
            modified_date=datetime_utils.get_iso_date(),
            has_machine=has_machine,
            has_squad=has_squad,
            managed=group.state.managed,
            justification=justification,
            modified_by=email,
            service=service,
            status=GroupStateStatus.ACTIVE,
            tags=group.state.tags,
            tier=tier,
            type=subscription,
        ),
    )
    if has_arm:
        await notifications_domain.update_group(
            loaders=loaders,
            comments=comments,
            group_name=group_name,
            group_state=group.state,
            had_arm=True,
            has_arm=has_arm,
            has_machine=has_machine,
            has_squad=has_squad,
            reason=justification.value,
            requester_email=email,
            service=service.value if service else "",
            subscription=str(subscription.value).lower(),
        )
        return

    await remove_group(
        loaders=loaders,
        group_name=group_name,
        justification=justification,
        email=email,
    )
    await notifications_domain.delete_group(
        loaders=loaders,
        deletion_date=datetime_utils.get_now_as_str(),
        group_name=group_name,
        requester_email=email,
        reason=justification.value,
    )


async def update_group_tier(
    *,
    loaders: Dataloaders,
    comments: str,
    email: str,
    group_name: str,
    tier: GroupTier,
) -> None:
    """Set a new tier for a group."""
    if tier == GroupTier.MACHINE:
        subscription = GroupSubscriptionType.CONTINUOUS
        has_machine = True
        has_squad = False
        service = GroupService.WHITE
    elif tier == GroupTier.SQUAD:
        subscription = GroupSubscriptionType.CONTINUOUS
        has_machine = True
        has_squad = True
        service = GroupService.WHITE
    elif tier == GroupTier.ONESHOT:
        subscription = GroupSubscriptionType.ONESHOT
        has_machine = False
        has_squad = False
        service = GroupService.BLACK
    elif tier == GroupTier.FREE:
        subscription = GroupSubscriptionType.CONTINUOUS
        has_machine = False
        has_squad = False
        service = GroupService.WHITE
    else:
        raise InvalidGroupTier()

    await update_group(
        loaders=loaders,
        comments=comments,
        email=email,
        group_name=group_name,
        justification=GroupStateUpdationJustification.OTHER,
        has_arm=True,
        has_machine=has_machine,
        has_squad=has_squad,
        service=service,
        subscription=subscription,
        tier=tier,
    )


async def get_closed_vulnerabilities(
    loaders: Dataloaders, group_name: str
) -> int:
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    findings_vulns: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in group_findings]
    )

    last_approved_status = [vuln.state.status for vuln in findings_vulns]
    return last_approved_status.count(VulnerabilityStateStatus.CLOSED)


async def get_groups_by_stakeholder(
    loaders: Dataloaders,
    email: str,
    active: bool = True,
    organization_id: str = "",
) -> list[str]:
    group_names = await group_access_domain.get_stakeholder_groups_names(
        loaders, email, active
    )
    if organization_id:
        org_groups = await loaders.organization_groups.load(organization_id)
        org_group_names: set[str] = set(group.name for group in org_groups)
        group_names = [
            group_name
            for group_name in group_names
            if group_name in org_group_names
        ]

    group_level_roles = await authz.get_group_level_roles(
        loaders, email, group_names
    )

    return [
        group_name
        for role, group_name in zip(group_level_roles.values(), group_names)
        if bool(role)
    ]


async def get_vulnerabilities_with_pending_attacks(
    *,
    loaders: Dataloaders,
    group_name: str,
) -> int:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    vulnerabilities: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in findings]
    )
    return len(
        tuple(
            vulnerability
            for vulnerability in vulnerabilities
            if vulnerability.verification
            and vulnerability.verification.status
            == VulnerabilityVerificationStatus.REQUESTED
        )
    )


async def get_max_severity(
    loaders: Dataloaders,
    group_name: str,
) -> Decimal:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    max_severity: Decimal = max(
        map(
            lambda finding: findings_domain.get_severity_score(
                finding.severity
            ),
            findings,
        ),
        default=Decimal("0.0"),
    )
    return Decimal(max_severity).quantize(Decimal("0.1"))


async def get_mean_remediate_severity_cvssf(
    loaders: Dataloaders,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: Optional[date] = None,
) -> Decimal:
    group_findings_loader = loaders.group_findings
    group_findings: tuple[Finding, ...] = await group_findings_loader.load(
        group_name.lower()
    )
    group_findings_ids: list[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= findings_domain.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    finding_cvssf: dict[str, Decimal] = {
        finding.id: vulns_utils.get_cvssf(
            findings_domain.get_severity_score(finding.severity)
        )
        for finding in group_findings
    }
    findings_vulns: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load_many_chained(
        group_findings_ids
    )
    return vulns_utils.get_mean_remediate_vulnerabilities_cvssf(
        findings_vulns,
        finding_cvssf,
        min_date,
    )


async def get_mean_remediate_non_treated_severity_cvssf(
    loaders: Dataloaders,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: Optional[date] = None,
) -> Decimal:
    group_findings_loader = loaders.group_findings
    group_findings: tuple[Finding, ...] = await group_findings_loader.load(
        group_name.lower()
    )
    group_findings_ids: list[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= findings_domain.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    finding_cvssf: dict[str, Decimal] = {
        finding.id: vulns_utils.get_cvssf(
            findings_domain.get_severity_score(finding.severity)
        )
        for finding in group_findings
    }
    findings_vulns: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load_many_chained(
        group_findings_ids
    )
    non_confirmed_zr_vulns = vulns_utils.filter_non_confirmed_zero_risk(
        findings_vulns
    )
    non_accepted_undefined_vulns = tuple(
        vuln
        for vuln in non_confirmed_zr_vulns
        if not vulns_utils.is_accepted_undefined_vulnerability(vuln)
    )
    return vulns_utils.get_mean_remediate_vulnerabilities_cvssf(
        non_accepted_undefined_vulns,
        finding_cvssf,
        min_date,
    )


async def get_mean_remediate_severity(
    loaders: Dataloaders,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: Optional[date] = None,
) -> Decimal:
    """Get mean time to remediate."""
    group_findings_loader = loaders.group_findings

    group_findings: tuple[Finding, ...] = await group_findings_loader.load(
        group_name.lower()
    )
    group_findings_ids: list[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= findings_domain.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    findings_vulns: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load_many_chained(
        group_findings_ids
    )
    return vulns_utils.get_mean_remediate_vulnerabilities(
        findings_vulns,
        min_date,
    )


async def get_mean_remediate_non_treated_severity(
    loaders: Dataloaders,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: Optional[date] = None,
) -> Decimal:
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name.lower()
    )
    group_findings_ids: list[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= findings_domain.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    findings_vulns: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load_many_chained(
        group_findings_ids
    )
    non_confirmed_zr_vulns = vulns_utils.filter_non_confirmed_zero_risk(
        findings_vulns
    )
    non_accepted_undefined_vulns = tuple(
        vuln
        for vuln in non_confirmed_zr_vulns
        if not vulns_utils.is_accepted_undefined_vulnerability(vuln)
    )
    return vulns_utils.get_mean_remediate_vulnerabilities(
        non_accepted_undefined_vulns,
        min_date,
    )


async def get_open_findings(loaders: Dataloaders, group_name: str) -> int:
    group_findings_loader = loaders.group_findings
    group_findings: tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    finding_status = await collect(
        tuple(
            findings_domain.get_status(loaders, finding.id)
            for finding in group_findings
        ),
        workers=32,
    )
    return finding_status.count("open")


async def get_open_vulnerabilities(
    loaders: Dataloaders,
    group_name: str,
) -> int:
    group_findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    findings_vulns: tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in group_findings]
    )

    last_approved_status = [vuln.state.status for vuln in findings_vulns]
    return last_approved_status.count(VulnerabilityStateStatus.OPEN)


async def invite_to_group(
    *,
    loaders: Dataloaders,
    email: str,
    responsibility: str,
    role: str,
    group_name: str,
    modified_by: str,
) -> None:
    group: Group = await loaders.group.load(group_name)
    if (
        not validate_field_length(responsibility, 50)
        or not validate_alphanumeric_field(responsibility)
        or not validate_email_address(email)
        or not validate_role_fluid_reqs(email, role)
        or not authz.validate_fluidattacks_staff_on_group(group, email, role)
    ):
        return

    expiration_time = datetime_utils.get_as_epoch(
        datetime_utils.get_now_plus_delta(weeks=1)
    )
    url_token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload={
            "group_name": group_name,
            "user_email": email,
        },
        subject="starlette_session",
    )
    await group_access_domain.update(
        loaders=loaders,
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(
            expiration_time=expiration_time,
            has_access=False,
            invitation=GroupInvitation(
                is_used=False,
                responsibility=responsibility,
                role=role,
                url_token=url_token,
            ),
            responsibility=responsibility,
            role=role,
            state=GroupAccessState(
                modified_date=datetime_utils.get_iso_date()
            ),
        ),
    )
    confirm_access_url = f"{BASE_URL}/confirm_access/{url_token}"
    reject_access_url = f"{BASE_URL}/reject_access/{url_token}"
    mail_to = [email]
    email_context: dict[str, Any] = {
        "admin": email,
        "group": group_name,
        "responsible": modified_by,
        "group_description": group.description,
        "confirm_access_url": confirm_access_url,
        "reject_access_url": reject_access_url,
        "user_role": role.replace("_", " "),
    }
    schedule(
        groups_mail.send_mail_access_granted(loaders, mail_to, email_context)
    )


async def exists(
    loaders: Dataloaders,
    group_name: str,
) -> bool:
    try:
        await loaders.group.load(group_name)
        return True
    except GroupNotFound:
        return False


async def is_valid(
    loaders: Dataloaders,
    group_name: str,
) -> bool:
    if await exists(loaders, group_name):
        group: Group = await loaders.group.load(group_name)
        if group.state.status == GroupStateStatus.ACTIVE:
            return True
    return False


async def mask_files(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    group: Group = await loaders.group.load(group_name)
    resources_files = await resources_utils.search_file(f"{group_name}/")
    if resources_files:
        await collect(
            resources_utils.remove_file(file_name)
            for file_name in resources_files
        )
    if group.files:
        masked_files: list[GroupFile] = [
            GroupFile(
                description=MASKED,
                file_name=MASKED,
                modified_by=MASKED,
                modified_date=file.modified_date,
            )
            for file in group.files
        ]
        await update_metadata(
            group_name=group_name,
            metadata=GroupMetadataToUpdate(files=masked_files),
            organization_id=group.organization_id,
        )


async def add_file(
    *,
    loaders: Dataloaders,
    description: str,
    email: str,
    file_name: str,
    group_name: str,
) -> None:
    group: Group = await loaders.group.load(group_name)
    modified_date: str = datetime_utils.get_iso_date()
    validations.validate_fields([description])
    validations.validate_field_length(description, 200)
    validations.validate_file_name(file_name)
    validations.validate_file_exists(file_name, group.files)
    group_file_to_add = GroupFile(
        description=description,
        file_name=file_name,
        modified_by=email,
        modified_date=modified_date,
    )
    if not group.files:
        files_to_update: list[GroupFile] = []
    else:
        files_to_update = group.files
        await send_mail_file_report(
            loaders=loaders,
            group_name=group_name,
            responsible=email,
            file_name=file_name,
            file_description=description,
            is_added=True,
            modified_date=modified_date,
        )
    files_to_update.append(group_file_to_add)
    await update_metadata(
        group_name=group_name,
        metadata=GroupMetadataToUpdate(
            files=files_to_update,
        ),
        organization_id=group.organization_id,
    )


async def remove_file(
    *,
    loaders: Dataloaders,
    email: str,
    file_name: str,
    group_name: str,
) -> None:
    group: Group = await loaders.group.load(group_name)
    if not group.files:
        raise ErrorUpdatingGroup.new()

    file_to_remove: Optional[GroupFile] = next(
        (file for file in group.files if file.file_name == file_name), None
    )
    if not file_to_remove:
        raise ErrorUpdatingGroup.new()

    file_url = f"{group_name}/{file_name}"
    await resources_utils.remove_file(file_url)
    await update_metadata(
        group_name=group_name,
        metadata=GroupMetadataToUpdate(
            files=[
                file
                for file in group.files
                if file.file_name != file_to_remove.file_name
            ]
        ),
        organization_id=group.organization_id,
    )
    uploaded_date = (
        datetime_utils.get_date_from_iso_str(file_to_remove.modified_date)
        if file_to_remove.modified_date
        else None
    )
    await send_mail_file_report(
        loaders=loaders,
        group_name=group_name,
        responsible=email,
        file_name=file_name,
        file_description=file_to_remove.description,
        modified_date=datetime_utils.get_iso_date(),
        uploaded_date=uploaded_date,
    )


async def send_mail_file_report(
    *,
    loaders: Dataloaders,
    group_name: str,
    responsible: str,
    file_name: str,
    file_description: str,
    is_added: bool = False,
    modified_date: str,
    uploaded_date: Optional[date] = None,
) -> None:
    roles: set[str] = {
        "resourcer",
        "customer_manager",
        "user_manager",
        "hacker",
    }
    stakeholders_email = (
        await group_access_domain.get_stakeholders_email_by_preferences(
            loaders=loaders,
            group_name=group_name,
            notification=Notification.FILE_UPDATE,
            roles=roles,
        )
    )

    await groups_mail.send_mail_file_report(
        loaders=loaders,
        group_name=group_name,
        responsible=responsible,
        is_added=is_added,
        file_name=file_name,
        file_description=file_description,
        report_date=datetime_utils.get_datetime_from_iso_str(modified_date),
        email_to=stakeholders_email,
        uploaded_date=uploaded_date,
    )


async def remove_all_stakeholders(
    *,
    loaders: Dataloaders,
    group_name: str,
    modified_by: str,
) -> None:
    """Revoke stakeholders access to group."""
    stakeholders_access: tuple[
        GroupAccess, ...
    ] = await loaders.group_stakeholders_access.load(group_name)
    await collect(
        tuple(
            remove_stakeholder(
                loaders=loaders,
                email_to_revoke=access.email,
                group_name=group_name,
                modified_by=modified_by,
            )
            for access in stakeholders_access
        )
    )


async def remove_all_roots(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
) -> None:
    await collect(
        tuple(
            roots_domain.remove_root(
                email=email,
                group_name=group_name,
                reason="GROUP_DELETED",
                root=root,
            )
            for root in await loaders.group_roots.load(group_name)
        )
    )


async def remove_resources(
    *,
    loaders: Dataloaders,
    group_name: str,
    email: str,
) -> None:
    all_findings = await loaders.group_drafts_and_findings.load(group_name)
    await collect(
        tuple(
            findings_domain.mask_finding(loaders, finding, email)
            for finding in all_findings
        ),
        workers=4,
    )
    group_events: tuple[Event, ...] = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    await collect(
        tuple(
            events_domain.remove_event(event.id, group_name)
            for event in group_events
        ),
        workers=4,
    )
    await group_comments_domain.remove_comments(group_name)
    await mask_files(loaders, group_name)
    await remove_all_roots(
        loaders=loaders,
        email=email,
        group_name=group_name,
    )
    await toe_inputs_model.remove_group_toe_inputs(group_name=group_name)
    await toe_lines_model.remove_group_toe_lines(group_name=group_name)
    await forces_model.remove_group_forces_executions(group_name=group_name)
    await groups_model.remove(group_name=group_name)


async def remove_stakeholder(
    *,
    loaders: Dataloaders,
    email_to_revoke: str,
    group_name: str,
    modified_by: str,
) -> None:
    """Remove stakeholder access to group."""
    await group_access_domain.remove_access(
        loaders, email_to_revoke, group_name
    )

    group: Group = await loaders.group.load(group_name)
    organization_id = group.organization_id
    has_org_access, stakeholder_groups_names = await collect(
        (
            orgs_domain.has_access(loaders, organization_id, email_to_revoke),
            get_groups_by_stakeholder(loaders, email_to_revoke),
        )
    )
    org_groups_names = set(
        group.name
        for group in await loaders.organization_groups.load(organization_id)
    )
    stakeholder_org_groups_names = set(
        stakeholder_groups_names  # type: ignore
    ).intersection(org_groups_names)
    stakeholder_org_groups: tuple[Group, ...] = await loaders.group.load_many(
        stakeholder_org_groups_names
    )
    has_groups_in_org = bool(
        groups_utils.filter_active_groups(stakeholder_org_groups)
    )
    if has_org_access and not has_groups_in_org:
        await orgs_domain.remove_access(
            loaders, organization_id, email_to_revoke, modified_by
        )

    all_groups_by_stakeholder = await loaders.group.load_many(
        stakeholder_groups_names
    )
    all_active_groups_by_stakeholder = groups_utils.filter_active_groups(
        all_groups_by_stakeholder
    )
    has_groups_in_asm = bool(all_active_groups_by_stakeholder)
    if not has_groups_in_asm:
        await stakeholders_domain.remove(email_to_revoke)


async def unsubscribe_from_group(
    *,
    loaders: Dataloaders,
    group_name: str,
    email: str,
) -> None:
    await remove_stakeholder(
        loaders=loaders,
        email_to_revoke=email,
        group_name=group_name,
        modified_by=email,
    )
    await send_mail_unsubscribed(
        loaders=loaders,
        group_name=group_name,
        email=email,
    )


async def send_mail_unsubscribed(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
) -> None:
    report_date: str = datetime_utils.get_iso_date()
    roles: set[str] = {"resourcer", "customer_manager", "user_manager"}
    stakeholders_email = (
        await group_access_domain.get_stakeholders_email_by_preferences(
            loaders=loaders,
            group_name=group_name,
            notification=Notification.UNSUBSCRIPTION_ALERT,
            roles=roles,
        )
    )

    await groups_mail.send_mail_stakeholder_unsubscribed(
        loaders=loaders,
        email=email,
        email_to=stakeholders_email,
        group_name=group_name,
        report_date=datetime_utils.get_datetime_from_iso_str(report_date),
    )


async def update_metadata(
    *,
    group_name: str,
    metadata: GroupMetadataToUpdate,
    organization_id: str,
) -> None:
    await groups_model.update_metadata(
        group_name=group_name,
        metadata=metadata,
        organization_id=organization_id,
    )


async def update_group_info(
    *,
    loaders: Dataloaders,
    group_name: str,
    metadata: GroupMetadataToUpdate,
    email: str,
) -> None:
    group: Group = await loaders.group.load(group_name)

    roles: set[str] = {"resourcer", "customer_manager", "user_manager"}
    stakeholders_email = (
        await group_access_domain.get_stakeholders_email_by_preferences(
            loaders=loaders,
            group_name=group_name,
            notification=Notification.GROUP_INFORMATION,
            roles=roles,
        )
    )

    await update_metadata(
        group_name=group_name,
        metadata=metadata,
        organization_id=group.organization_id,
    )

    if metadata:
        await groups_mail.send_mail_updated_group_information(
            loaders=loaders,
            group_name=group_name,
            responsible=email,
            group=group,
            metadata=metadata,
            report_date=datetime_utils.get_iso_date(),
            email_to=stakeholders_email,
        )


async def update_forces_access_token(
    *,
    loaders: Dataloaders,
    group_name: str,
    email: str,
    expiration_time: int,
    responsible: str,
) -> str:
    group: Group = await loaders.group.load(group_name)
    had_token: bool = bool(group.agent_token)

    result = await stakeholders_domain.update_access_token(
        email, expiration_time
    )
    await send_mail_devsecops_agent(
        loaders=loaders,
        group_name=group_name,
        responsible=responsible,
        had_token=had_token,
    )

    return result


async def send_mail_devsecops_agent(
    *,
    loaders: Dataloaders,
    group_name: str,
    responsible: str,
    had_token: bool,
) -> None:
    report_date: str = datetime_utils.get_iso_date()
    roles: set[str] = {"resourcer", "customer_manager", "user_manager"}
    stakeholders_email = (
        await group_access_domain.get_stakeholders_email_by_preferences(
            loaders=loaders,
            group_name=group_name,
            notification=Notification.AGENT_TOKEN,
            roles=roles,
        )
    )

    await groups_mail.send_mail_devsecops_agent_token(
        loaders=loaders,
        email=responsible,
        email_to=stakeholders_email,
        group_name=group_name,
        had_token=had_token,
        report_date=datetime_utils.get_datetime_from_iso_str(report_date),
    )


async def update_state(
    *,
    group_name: str,
    state: GroupState,
    organization_id: str,
) -> None:
    await groups_model.update_state(
        group_name=group_name, state=state, organization_id=organization_id
    )


async def update_indicators(
    *,
    group_name: str,
    indicators: GroupUnreliableIndicators,
) -> None:
    await groups_model.update_unreliable_indicators(
        group_name=group_name, indicators=indicators
    )


async def set_pending_deletion_date(
    group: Group,
    modified_by: str,
    pending_deletion_date: str,
) -> None:
    """Update pending deletion date in group's state."""
    await update_state(
        group_name=group.name,
        organization_id=group.organization_id,
        state=group.state._replace(
            modified_by=modified_by,
            modified_date=datetime_utils.get_iso_date(),
            pending_deletion_date=pending_deletion_date,
        ),
    )


async def remove_pending_deletion_date(
    group: Group,
    modified_by: str,
) -> None:
    """Clear pending deletion date in group's state."""
    await update_state(
        group_name=group.name,
        organization_id=group.organization_id,
        state=group.state._replace(
            modified_by=modified_by,
            modified_date=datetime_utils.get_iso_date(),
            pending_deletion_date="",
        ),
    )


async def update_group_tags(
    *,
    loaders: Dataloaders,
    group_name: str,
    email: str,
    updated_tags: set[str],
) -> None:
    group: Group = await loaders.group.load(group_name)

    if updated_tags != group.state.tags:
        await update_state(
            group_name=group_name,
            organization_id=group.organization_id,
            state=GroupState(
                comments=group.state.comments,
                modified_date=datetime_utils.get_iso_date(),
                has_machine=group.state.has_machine,
                has_squad=group.state.has_squad,
                managed=group.state.managed,
                payment_id=group.state.payment_id,
                justification=GroupStateUpdationJustification["NONE"],
                modified_by=email,
                service=group.state.service,
                status=GroupStateStatus.ACTIVE,
                tags=updated_tags,
                tier=group.state.tier,
                type=group.state.type,
            ),
        )


async def add_tags(
    *,
    loaders: Dataloaders,
    email: str,
    group: Group,
    tags_to_add: set[str],
) -> None:
    updated_tags = (
        group.state.tags.union(tags_to_add)
        if group.state.tags
        else tags_to_add
    )
    await update_group_tags(
        loaders=loaders,
        group_name=group.name,
        email=email,
        updated_tags=updated_tags,
    )
    schedule(
        send_mail_portfolio_report(
            loaders=loaders,
            group_name=group.name,
            responsible=email,
            portfolio=", ".join(tags_to_add),
            is_added=True,
            modified_date=datetime_utils.get_iso_date(),
        )
    )


async def remove_tag(
    *,
    loaders: Dataloaders,
    email: str,
    group: Group,
    tag_to_remove: str,
) -> None:
    if group.state.tags:
        updated_tags: set[str] = {
            tag for tag in group.state.tags if tag != tag_to_remove
        }
        await update_group_tags(
            loaders=loaders,
            group_name=group.name,
            email=email,
            updated_tags=updated_tags,
        )
        schedule(
            send_mail_portfolio_report(
                loaders=loaders,
                group_name=group.name,
                responsible=email,
                portfolio=tag_to_remove,
                modified_date=datetime_utils.get_iso_date(),
            )
        )


async def send_mail_portfolio_report(
    *,
    loaders: Dataloaders,
    group_name: str,
    responsible: str,
    portfolio: str,
    is_added: bool = False,
    modified_date: str,
) -> None:
    roles: set[str] = {"resourcer", "customer_manager", "user_manager"}
    stakeholders_email = (
        await group_access_domain.get_stakeholders_email_by_preferences(
            loaders=loaders,
            group_name=group_name,
            notification=Notification.PORTFOLIO_UPDATE,
            roles=roles,
        )
    )

    await groups_mail.send_mail_portfolio_report(
        loaders=loaders,
        group_name=group_name,
        responsible=responsible,
        is_added=is_added,
        portfolio=portfolio,
        report_date=datetime_utils.get_date_from_iso_str(modified_date),
        email_to=stakeholders_email,
    )


def validate_group_services_config(
    has_machine: bool,
    has_squad: bool,
    has_arm: bool,
) -> None:
    if has_squad:
        if not has_arm:
            raise InvalidGroupServicesConfig(
                "Squad is only available when ASM is too"
            )
        if not has_machine:
            raise InvalidGroupServicesConfig(
                "Squad is only available when Machine is too"
            )


async def validate_group_tags(
    loaders: Dataloaders, group_name: str, tags: list[str]
) -> list[str]:
    """Validate tags array."""
    pattern = re.compile("^[a-z0-9]+(?:-[a-z0-9]+)*$")
    if await _has_repeated_tags(loaders, group_name, tags):
        raise RepeatedValues()
    return [tag for tag in tags if pattern.match(tag)]


async def request_upgrade(
    *,
    loaders: Dataloaders,
    email: str,
    group_names: list[str],
) -> None:
    """
    Lead the stakeholder towards a subscription upgrade managed by our team.
    This is meant to be a temporary flow while the billing module gets ready.
    """
    enforcer = await authz.get_group_level_enforcer(loaders, email)
    if not all(
        enforcer(group_name, "request_group_upgrade")
        for group_name in group_names
    ):
        raise GroupNotFound()

    groups: tuple[Group, ...] = await loaders.group.load_many(group_names)
    if any(group.state.has_squad for group in groups):
        raise BillingSubscriptionSameActive()

    await notifications_domain.request_groups_upgrade(loaders, email, groups)


async def get_treatment_summary(
    loaders: Dataloaders,
    group_name: str,
) -> GroupTreatmentSummary:
    """Get the total vulnerability treatment."""
    findings = await loaders.group_findings.load(group_name)
    non_deleted_findings = tuple(
        finding
        for finding in findings
        if not findings_domain.is_deleted(finding)
    )
    finding_vulns_loader = loaders.finding_vulnerabilities_nzr
    vulns: tuple[
        Vulnerability, ...
    ] = await finding_vulns_loader.load_many_chained(
        [finding.id for finding in non_deleted_findings]
    )
    treatment_counter = Counter(
        vuln.treatment.status
        for vuln in vulns
        if vuln.treatment
        and vuln.state.status == VulnerabilityStateStatus.OPEN
    )
    return GroupTreatmentSummary(
        accepted=treatment_counter[VulnerabilityTreatmentStatus.ACCEPTED],
        accepted_undefined=treatment_counter[
            VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED
        ],
        in_progress=treatment_counter[
            VulnerabilityTreatmentStatus.IN_PROGRESS
        ],
        new=treatment_counter[VulnerabilityTreatmentStatus.NEW],
    )


async def get_oldest_finding_date(
    loaders: Dataloaders, group_name: str
) -> Optional[datetime]:
    findings: tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    ages: list[datetime] = [
        datetime.fromisoformat(
            finding.unreliable_indicators.unreliable_oldest_vulnerability_report_date  # noqa
        )
        for finding in findings
        if finding.unreliable_indicators.unreliable_oldest_vulnerability_report_date  # noqa
    ]
    if ages:
        return min(ages)
    return None


async def update_policies(
    *,
    loaders: Dataloaders,
    email: str,
    group_name: str,
    organization_id: str,
    policies_to_update: PoliciesToUpdate,
) -> None:
    validated_policies: dict[str, Any] = {}
    for attr, value in policies_to_update._asdict().items():
        if value is not None:
            value = (
                Decimal(value).quantize(Decimal("0.1"))
                if isinstance(value, float)
                else Decimal(value)
            )
            validated_policies[attr] = value
            validator_func = getattr(orgs_domain, f"validate_{attr}")
            validator_func(value)
    await validate_acceptance_severity_range(
        group_name=group_name, loaders=loaders, values=policies_to_update
    )

    if validated_policies:
        today = datetime_utils.get_iso_date()
        await groups_model.update_policies(
            group_name=group_name,
            modified_by=email,
            modified_date=today,
            organization_id=organization_id,
            policies=policies_to_update,
        )
        schedule(
            send_mail_policies(
                group_name=group_name,
                loaders=loaders,
                modified_date=today,
                new_policies=policies_to_update._asdict(),
                responsible=email,
            )
        )


async def validate_acceptance_severity_range(
    *, group_name: str, loaders: Dataloaders, values: PoliciesToUpdate
) -> bool:
    success: bool = True
    group: Group = await loaders.group.load(group_name)
    min_acceptance_severity = (
        await groups_utils.get_group_min_acceptance_severity(
            loaders=loaders,
            group=group,
        )
    )
    max_acceptance_severity = (
        await groups_utils.get_group_max_acceptance_severity(
            loaders=loaders,
            group=group,
        )
    )
    min_value = (
        values.min_acceptance_severity
        if values.min_acceptance_severity is not None
        else min_acceptance_severity
    )
    max_value = (
        values.max_acceptance_severity
        if values.max_acceptance_severity is not None
        else max_acceptance_severity
    )
    if (
        min_value is not None
        and max_value is not None
        and (min_value > max_value)
    ):
        raise InvalidAcceptanceSeverityRange()
    return success


async def send_mail_policies(
    *,
    group_name: str,
    loaders: Dataloaders,
    modified_date: str,
    new_policies: dict[str, Any],
    responsible: str,
) -> None:
    group_data: Group = await loaders.group.load(group_name)
    organization_data: Organization = await loaders.organization.load(
        group_data.organization_id
    )

    policies_content: dict[str, Any] = {}
    for key, val in new_policies.items():
        old_value = (
            group_data.policies._asdict().get(key)
            if group_data.policies
            else organization_data.policies._asdict().get(key)
        )
        if val is not None and val != old_value:
            policies_content[POLICIES_FORMATTED[key]] = {
                "from": old_value,
                "to": val,
            }

    email_context: dict[str, Any] = {
        "entity_name": group_name,
        "policies_link": (
            f"{BASE_URL}/orgs/{organization_data.name}"
            f"/groups/{group_name}/scope"
        ),
        "policies_content": policies_content,
        "responsible": responsible,
        "date": datetime_utils.get_datetime_from_iso_str(modified_date),
    }
    group_stakeholders: tuple[
        Stakeholder, ...
    ] = await group_access_domain.get_group_stakeholders(loaders, group_name)

    stakeholders_emails = [
        stakeholder.email
        for stakeholder in group_stakeholders
        if await group_access_domain.get_stakeholder_role(
            loaders, stakeholder.email, group_name, stakeholder.is_registered
        )
        in ["customer_manager", "user_manager"]
    ]

    if policies_content:
        await groups_mail.send_mail_updated_policies(
            loaders=loaders,
            email_to=stakeholders_emails,
            context=email_context,
        )
