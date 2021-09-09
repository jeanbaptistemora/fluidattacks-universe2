# pylint:disable=too-many-lines

from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
    schedule,
)
import authz
import bugsnag
from collections import (
    Counter,
    defaultdict,
    namedtuple,
)
from context import (
    BASE_URL,
    FI_API_STATUS,
    FI_DEFAULT_ORG,
)
from contextlib import (
    AsyncExitStack,
)
from custom_exceptions import (
    AlreadyPendingDeletion,
    InvalidGroupName,
    InvalidGroupServicesConfig,
    InvalidParameter,
    RepeatedValues,
    UserNotInOrganization,
)
from custom_types import (
    Group as GroupType,
    GroupAccess as GroupAccessType,
    Historic as HistoricType,
    Invitation as InvitationType,
    MailContent as MailContentType,
    User as UserType,
)
from datetime import (
    date,
)
from db_model.findings.types import (
    Finding,
)
from decimal import (
    Decimal,
)
from dynamodb import (
    model as dynamomodel,
)
from dynamodb.operations_legacy import (
    start_context,
)
from dynamodb.types import (
    GroupMetadata,
)
from events import (
    domain as events_domain,
)
from findings import (
    domain as findings_domain,
)
from findings.domain import (
    get_max_open_severity,
    get_max_open_severity_new,
    get_oldest_no_treatment,
    get_oldest_no_treatment_new,
)
from group_access import (
    domain as group_access_domain,
)
from group_comments.domain import (
    get_total_comments_date,
    mask_comments,
)
from groups import (
    dal as groups_dal,
)
import logging
import logging.config
from mailer import (
    groups as groups_mail,
)
from names import (
    domain as names_domain,
)
from newutils import (
    apm,
    datetime as datetime_utils,
    events as events_utils,
    resources as resources_utils,
    vulnerabilities as vulns_utils,
)
from newutils.utils import (
    get_key_or_fallback,
)
from newutils.validations import (
    validate_alphanumeric_field,
    validate_email_address,
    validate_field_length,
    validate_fields,
    validate_group_name,
    validate_phone_field,
    validate_string_length_between,
)
from notifications import (
    domain as notifications_domain,
)
from operator import (
    itemgetter,
)
from organizations import (
    domain as orgs_domain,
)
import re
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from roots import (
    domain as roots_domain,
)
import secrets
from settings import (
    LOGGING,
    NOEXTRA,
)
from typing import (
    Any,
    Awaitable,
    cast,
    Dict,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Union,
)
from users import (
    domain as users_domain,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


def _process_digest_reattacks_requested(
    reattacks_requested: int, groups_stats: Tuple[MailContentType]
) -> MailContentType:
    """Process digest reattacks requested sub-section"""
    requested: MailContentType = {
        "groups_requested": list(),
    }
    if not reattacks_requested:
        # Get groups with oldest date since last request
        groups_requested_date = [
            {
                "age_last_requested": (
                    datetime_utils.get_now()
                    - datetime_utils.get_from_str(
                        group["reattacks"]["last_requested_date"]
                    )
                ).days,
                "group": group["group"],
            }
            for group in groups_stats
            if not group["reattacks"]["reattacks_requested"]
            and group["reattacks"]["last_requested_date"]
        ]
        # Filter out those with 0 age
        groups_requested_date = [
            group
            for group in groups_requested_date
            if group["age_last_requested"]
        ]
        requested["groups_requested"] = sorted(
            groups_requested_date,
            key=itemgetter("age_last_requested"),
            reverse=True,
        )[:3]
    else:
        # Get groups with most reattacks requested
        groups_requested = [
            {
                "reattacks_requested": group["reattacks"][
                    "reattacks_requested"
                ],
                "group": group["group"],
            }
            for group in groups_stats
            if group["reattacks"]["reattacks_requested"]
        ]
        requested["groups_requested"] = sorted(
            groups_requested,
            key=itemgetter("reattacks_requested"),
            reverse=True,
        )[:3]

    return requested


def _process_digest_reattacks_executed(
    reattacks_executed: int,
    reattacks_executed_total: int,
    effective_reattacks_total: int,
    groups_stats: Tuple[MailContentType],
) -> MailContentType:
    """Process digest reattacks executed sub-section"""
    executed: MailContentType = {
        "groups_executed": list(),
    }
    if not reattacks_executed:
        # Get groups with oldest date since last reattack
        groups_executed_date = [
            {
                "age_last_executed": (
                    datetime_utils.get_now()
                    - datetime_utils.get_from_str(
                        group["reattacks"]["last_executed_date"]
                    )
                ).days,
                "group": group["group"],
            }
            for group in groups_stats
            if not group["reattacks"]["reattacks_executed"]
            and group["reattacks"]["last_executed_date"]
        ]
        # Filter out those with 0 age
        groups_executed_date = [
            group
            for group in groups_executed_date
            if group["age_last_executed"]
        ]
        executed["groups_executed"] = sorted(
            groups_executed_date,
            key=itemgetter("age_last_executed"),
            reverse=True,
        )[:3]
    else:
        # Get groups with most reattacks executed
        groups_executed = [
            {
                "reattacks_executed": group["reattacks"]["reattacks_executed"],
                "group": group["group"],
            }
            for group in groups_stats
            if group["reattacks"]["reattacks_executed"]
        ]
        executed["groups_executed"] = sorted(
            groups_executed, key=itemgetter("reattacks_executed"), reverse=True
        )[:3]

    # Also known as "remediation effectiveness"
    if reattacks_executed_total:
        executed["reattack_effectiveness"] = int(
            100 * effective_reattacks_total / reattacks_executed_total
        )

    return executed


def _process_digest_reattacks_pending(
    groups_stats: Tuple[MailContentType],
) -> MailContentType:
    """Process digest pending reattacks sub-section"""
    pending: MailContentType = {
        "groups_pending": list(),
    }
    # Get groups with most pending reattacks
    groups_pending = [
        {
            "pending_attacks": group["reattacks"]["pending_attacks"],
            "group": group["group"],
        }
        for group in groups_stats
        if group["reattacks"]["pending_attacks"]
    ]
    pending["groups_pending"] = sorted(
        groups_pending, key=itemgetter("pending_attacks"), reverse=True
    )[:3]

    return pending


def _process_digest_reattacks(
    groups_stats: Tuple[MailContentType],
) -> MailContentType:
    """Process digest reattacks section"""
    reattacks_count: Counter = Counter()
    for stat in groups_stats:
        reattacks_count.update(stat["reattacks"])
    reattacks = dict(reattacks_count)

    reattacks.update(
        _process_digest_reattacks_requested(
            reattacks["reattacks_requested"], groups_stats
        )
    )

    reattacks.update(
        _process_digest_reattacks_executed(
            reattacks["reattacks_executed"],
            reattacks["reattacks_executed_total"],
            reattacks["effective_reattacks_total"],
            groups_stats=groups_stats,
        )
    )

    if reattacks["pending_attacks"]:
        reattacks.update(_process_digest_reattacks_pending(groups_stats))

    # Remove unneeded keys
    reattacks.pop("last_requested_date", None)
    reattacks.pop("last_executed_date", None)

    return reattacks


def _process_digest_treatments(
    groups_stats: Tuple[MailContentType],
) -> MailContentType:
    """Process digest treatments section"""
    treatments_count: Counter = Counter()
    for stat in groups_stats:
        treatments_count.update(stat["treatments"])
    treatments = dict(treatments_count)

    # Get groups with most temporary applied
    temporary: MailContentType = {
        "groups_temporary": list(),
    }
    groups_temporary = [
        {
            "temporary_applied": group["treatments"]["temporary_applied"],
            "group": group["group"],
        }
        for group in groups_stats
        if group["treatments"]["temporary_applied"]
    ]
    temporary["groups_temporary"] = sorted(
        groups_temporary, key=itemgetter("temporary_applied"), reverse=True
    )[:3]
    treatments.update(temporary)

    # Get groups with most eternal requested
    eternal_requested: MailContentType = {
        "groups_eternal_requested": list(),
    }
    groups_eternal_requested = [
        {
            "eternal_requested": group["treatments"]["eternal_requested"],
            "group": group["group"],
        }
        for group in groups_stats
        if group["treatments"]["eternal_requested"]
    ]
    eternal_requested["groups_eternal_requested"] = sorted(
        groups_eternal_requested,
        key=itemgetter("eternal_requested"),
        reverse=True,
    )[:3]
    treatments.update(eternal_requested)

    # Get groups with most eternal approved
    eternal_approved: MailContentType = {
        "groups_eternal_approved": list(),
    }
    groups_eternal_approved = [
        {
            "eternal_approved": group["treatments"]["eternal_approved"],
            "group": group["group"],
        }
        for group in groups_stats
        if group["treatments"]["eternal_approved"]
    ]
    eternal_approved["groups_eternal_approved"] = sorted(
        groups_eternal_approved,
        key=itemgetter("eternal_approved"),
        reverse=True,
    )[:3]
    treatments.update(eternal_approved)

    return treatments


async def _has_repeated_tags(group_name: str, tags: List[str]) -> bool:
    has_repeated_tags = len(tags) != len(set(tags))
    if not has_repeated_tags:
        group_info = await get_attributes(group_name.lower(), ["tag"])
        existing_tags = group_info.get("tag", [])
        all_tags = list(existing_tags) + tags
        has_repeated_tags = len(all_tags) != len(set(all_tags))
    return has_repeated_tags


async def can_user_access(group: str, role: str) -> bool:
    return await groups_dal.can_user_access(group, role)


async def complete_register_for_group_invitation(
    group_access: GroupAccessType,
) -> bool:
    coroutines: List[Awaitable[bool]] = []
    success: bool = False
    invitation = cast(InvitationType, group_access["invitation"])
    if invitation["is_used"]:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    group_name = cast(str, get_key_or_fallback(group_access))
    phone_number = cast(str, invitation["phone_number"])
    responsibility = cast(str, invitation["responsibility"])
    role = cast(str, invitation["role"])
    user_email = cast(str, group_access["user_email"])
    updated_invitation = invitation.copy()
    updated_invitation["is_used"] = True

    coroutines.extend(
        [
            group_access_domain.update(
                user_email,
                group_name,
                {
                    "expiration_time": None,
                    "has_access": True,
                    "invitation": updated_invitation,
                    "responsibility": responsibility,
                },
            ),
            authz.grant_group_level_role(user_email, group_name, role),
        ]
    )

    organization_id = await orgs_domain.get_id_for_group(group_name)
    if not await orgs_domain.has_user_access(organization_id, user_email):
        coroutines.append(
            orgs_domain.add_user(organization_id, user_email, "customer")
        )

    if await users_domain.get_data(user_email, "email"):
        coroutines.append(
            users_domain.add_phone_to_user(user_email, phone_number)
        )
    else:
        coroutines.append(
            users_domain.create(user_email, {"phone": phone_number})
        )

    if not await users_domain.is_registered(user_email):
        coroutines.extend(
            [
                users_domain.register(user_email),
                authz.grant_user_level_role(user_email, "customer"),
            ]
        )

    success = all(await collect(coroutines))
    if success:
        redis_del_by_deps_soon(
            "confirm_access",
            group_name=group_name,
            organization_id=organization_id,
        )
    return success


async def add_group(  # pylint: disable=too-many-arguments,too-many-locals
    user_email: str,
    user_role: str,
    group_name: str,
    organization: str,
    description: str,
    service: str,
    has_machine: bool = False,
    has_squad: bool = False,
    subscription: str = "continuous",
    language: str = "en",
) -> bool:
    validate_group_name(group_name)
    validate_fields([description])
    validate_field_length(group_name, 20)
    validate_field_length(description, 200)

    is_user_admin = user_role == "admin"

    success: bool = False
    if description.strip() and group_name.strip():
        validate_group_services_config(
            has_machine,
            has_squad,
            has_asm=True,
        )
        is_group_avail, group_exists = await collect(
            [
                names_domain.exists(group_name, "group"),
                groups_dal.exists(group_name),
            ]
        )

        org_id = await orgs_domain.get_id_by_name(organization)
        if not await orgs_domain.has_user_access(org_id, user_email):
            raise UserNotInOrganization(org_id)

        if is_group_avail and not group_exists:
            group: GroupType = {
                # Compatibility with old API
                "project_name": group_name,
                "group_name": group_name,
                "description": description,
                "language": language,
                "historic_configuration": [
                    {
                        "date": datetime_utils.get_now_as_str(),
                        "has_skims": has_machine,
                        "has_drills": has_squad,
                        "has_forces": True,
                        "requester": user_email,
                        "service": service,
                        "type": subscription,
                    }
                ],
                "project_status": "ACTIVE",
                "group_status": "ACTIVE",
            }
            success = await groups_dal.add(group)
            await dynamomodel.create_group_metadata(
                group_metadata=GroupMetadata(
                    name=group_name,
                    description=description,
                    language=language,
                ),
            )
            if success:
                await collect(
                    (
                        orgs_domain.add_group(org_id, group_name),
                        names_domain.remove(group_name, "group"),
                    )
                )
                # Admins are not granted access to the group
                # they are omnipresent
                if not is_user_admin:
                    success = success and all(
                        await collect(
                            (
                                group_access_domain.update_has_access(
                                    user_email, group_name, True
                                ),
                                authz.grant_group_level_role(
                                    user_email, group_name, "group_manager"
                                ),
                            )
                        )
                    )
        else:
            raise InvalidGroupName()
    else:
        raise InvalidParameter()
    # Notify us in case the user wants any Fluid Service
    if success:
        await notifications_domain.new_group(
            description=description,
            group_name=group_name,
            has_machine=has_machine,
            has_squad=has_squad,
            organization=organization,
            requester_email=user_email,
            service=service,
            subscription=subscription,
        )
    return success


async def add_without_group(
    email: str,
    role: str,
    phone_number: str = "",
    should_add_default_org: bool = True,
) -> bool:
    success = False
    if validate_phone_field(phone_number) and validate_email_address(email):
        new_user_data: UserType = {}
        new_user_data["email"] = email
        new_user_data["authorized"] = True
        new_user_data["registered"] = True
        if phone_number:
            new_user_data["phone"] = phone_number

        success = all(
            await collect(
                [
                    authz.grant_user_level_role(email, role),
                    users_domain.create(email, new_user_data),
                ]
            )
        )
        org = await orgs_domain.get_or_add(FI_DEFAULT_ORG)
        if should_add_default_org and not await orgs_domain.has_user_access(
            str(org["id"]), email
        ):
            await orgs_domain.add_user(str(org["id"]), email, "customer")
    return success


async def remove_group(
    context: Any, group_name: str, user_email: str, organization_id: str
) -> bool:
    response = False
    data = await groups_dal.get_attributes(
        group_name, ["project_status", "historic_deletion"]
    )
    historic_deletion = cast(
        List[Dict[str, str]], data.get("historic_deletion", [])
    )
    if (
        get_key_or_fallback(data, "group_status", "project_status")
        != "DELETED"
    ):
        all_resources_removed = await remove_resources(context, group_name)
        today = datetime_utils.get_now()
        new_state = {
            "date": datetime_utils.get_as_str(today),
            "deletion_date": datetime_utils.get_as_str(today),
            "user": user_email.lower(),
        }
        historic_deletion.append(new_state)
        new_data: GroupType = {
            "historic_deletion": historic_deletion,
            "group_status": "DELETED",
            "project_status": "DELETED",
        }
        response = all(
            [all_resources_removed, await update(group_name, new_data)]
        )
        if response:
            group_roots_loader: DataLoader = context.group_roots
            all_group_roots = await group_roots_loader.load(group_name)
            other = ""
            reason = "GROUP_DELETED"
            await collect(
                [
                    roots_domain.deactivate_root(
                        group_name=group_name,
                        other=other,
                        reason=reason,
                        root=root,
                        user_email=user_email,
                    )
                    for root in all_group_roots
                ]
            )
    else:
        raise AlreadyPendingDeletion()
    if response:
        response = all(
            [
                await collect(
                    (
                        authz.revoke_cached_group_service_policies(group_name),
                        orgs_domain.remove_group(group_name, organization_id),
                    )
                )
            ]
        )
    return response


async def update_group_attrs(
    *,
    loaders: Any,
    comments: str,
    group_name: str,
    has_squad: bool,
    has_asm: bool,
    has_machine: bool,
    reason: str,
    requester_email: str,
    service: str,
    subscription: str,
) -> bool:
    success: bool = False

    validate_fields([comments])
    validate_string_length_between(comments, 0, 250)
    validate_group_services_config(
        has_machine,
        has_squad,
        has_asm,
    )

    item = await groups_dal.get_attributes(
        group_name=group_name,
        attributes=["historic_configuration", "project_name"],
    )
    item.setdefault("historic_configuration", [])

    if get_key_or_fallback(item):
        success = await update(
            data={
                "historic_configuration": cast(
                    List[Dict[str, Union[bool, str]]],
                    item["historic_configuration"],
                )
                + [
                    {
                        "comments": comments,
                        "date": datetime_utils.get_now_as_str(),
                        "has_skims": has_machine,
                        "has_machine": has_machine,
                        "has_drills": has_squad,
                        "has_squad": has_squad,
                        "has_forces": True,
                        "reason": reason,
                        "requester": requester_email,
                        "service": service,
                        "type": subscription,
                    }
                ],
            },
            group_name=group_name,
        )

    if not has_asm:
        group_loader = loaders.group
        group = await group_loader.load(group_name)
        org_id = group["organization"]
        success = success and await remove_group(
            loaders, group_name, requester_email, org_id
        )

    if success and has_asm:
        await notifications_domain.update_group(
            comments=comments,
            group_name=group_name,
            had_machine=cast(
                List[Dict[str, bool]], item["historic_configuration"]
            )[-1]["has_skims"],
            had_squad=(
                cast(
                    bool,
                    get_key_or_fallback(
                        cast(
                            List[Dict[str, Union[bool, str]]],
                            item["historic_configuration"],
                        )[-1],
                        "has_squad",
                        "has_drills",
                    ),
                )
                if item["historic_configuration"]
                else False
            ),
            had_asm=True,
            has_machine=has_machine,
            has_squad=has_squad,
            has_asm=has_asm,
            reason=reason,
            requester_email=requester_email,
            service=service,
            subscription=subscription,
        )
    elif success and not has_asm:
        await notifications_domain.delete_group(
            deletion_date=datetime_utils.get_now_as_str(),
            group_name=group_name,
            requester_email=requester_email,
            reason=reason,
        )
    return success


async def get_active_groups() -> List[str]:
    groups = await groups_dal.get_active_groups()
    return groups


async def get_alive_group_names() -> List[str]:
    attributes = ["project_name"]
    groups = await get_alive_groups(attributes)
    return [get_key_or_fallback(group) for group in groups]


async def get_all(attributes: Optional[List[str]] = None) -> List[GroupType]:
    data_attr = ",".join(attributes or [])
    return await groups_dal.get_all(data_attr=data_attr)


async def get_alive_groups(
    attributes: Optional[List[str]] = None,
) -> List[GroupType]:
    data_attr = ",".join(attributes or [])
    groups = await groups_dal.get_alive_groups(data_attr)
    return groups


async def get_attributes(
    group_name: str, attributes: List[str]
) -> Dict[str, Union[str, List[str]]]:
    return await groups_dal.get_attributes(group_name, attributes)


async def get_closed_vulnerabilities(context: Any, group_name: str) -> int:
    group_findings = await context.group_findings.load(group_name)
    findings_vulns = await context.finding_vulns_nzr.load_many_chained(
        [finding["finding_id"] for finding in group_findings]
    )

    last_approved_status = [
        vulns_utils.get_last_status(vuln) for vuln in findings_vulns
    ]
    return last_approved_status.count("closed")


async def get_closed_vulnerabilities_new(loaders: Any, group_name: str) -> int:
    group_findings_loader = loaders.group_findings_new
    group_findings_loader.clear(group_name)
    finding_vulns_loader = loaders.finding_vulns_nzr

    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    findings_vulns = await finding_vulns_loader.load_many_chained(
        [finding.id for finding in group_findings]
    )

    last_approved_status = [
        vulns_utils.get_last_status(vuln) for vuln in findings_vulns
    ]
    return last_approved_status.count("closed")


async def get_description(group_name: str) -> str:
    return await groups_dal.get_description(group_name)


@apm.trace()
async def get_groups_by_user(
    user_email: str, active: bool = True, organization_id: str = ""
) -> List[str]:
    user_groups: List[str] = []
    groups = await group_access_domain.get_user_groups(user_email, active)
    group_level_roles = await authz.get_group_level_roles(user_email, groups)
    can_access_list = await collect(
        can_user_access(group, role)
        for role, group in zip(group_level_roles.values(), groups)
    )
    user_groups = [
        group
        for can_access, group in zip(can_access_list, groups)
        if can_access
    ]

    if organization_id:
        org_groups = await orgs_domain.get_groups(organization_id)
        user_groups = [group for group in user_groups if group in org_groups]
    return user_groups


async def get_vulnerabilities_with_pending_attacks(
    *,
    loaders: Any,
    group_name: str,
) -> int:
    if FI_API_STATUS == "migration":
        findings_new: Tuple[
            Finding, ...
        ] = await loaders.group_findings_new.load(group_name)
        vulnerabilities = await loaders.finding_vulns_nzr.load_many_chained(
            [finding.id for finding in findings_new]
        )
    else:
        findings = await loaders.group_findings.load(group_name)
        vulnerabilities = await loaders.finding_vulns_nzr.load_many_chained(
            [str(finding["finding_id"]) for finding in findings]
        )
    return sum(
        vulnerability["verification"] == "Requested"
        for vulnerability in vulnerabilities
    )


async def get_groups_with_forces() -> List[str]:
    return await groups_dal.get_groups_with_forces()


async def get_many_groups(groups_name: List[str]) -> List[GroupType]:
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(groups_dal.TABLE_NAME)
        groups = await collect(
            groups_dal.get_group(group_name, table)
            for group_name in groups_name
        )
    return cast(List[GroupType], groups)


async def get_mean_remediate(
    context: Any, group_name: str, min_date: Optional[date] = None
) -> Decimal:
    group_findings = await context.group_findings.load(group_name)
    vulns = await context.finding_vulns.load_many_chained(
        [str(finding["finding_id"]) for finding in group_findings]
    )
    return vulns_utils.get_mean_remediate_vulnerabilities(vulns, min_date)


async def get_mean_remediate_new(
    loaders: Any,
    group_name: str,
    min_date: Optional[date] = None,
) -> Decimal:
    group_findings_loader = loaders.group_findings_new
    finding_vulns_loaders = loaders.finding_vulns

    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    vulns = await finding_vulns_loaders.load_many_chained(
        [finding.id for finding in group_findings]
    )
    return vulns_utils.get_mean_remediate_vulnerabilities(vulns, min_date)


async def get_mean_remediate_non_treated(
    loaders: Any, group_name: str, min_date: Optional[date] = None
) -> Decimal:
    findings = await loaders.group_findings.load(group_name)
    all_vulnerabilities = await loaders.finding_vulns.load_many_chained(
        [str(finding["finding_id"]) for finding in findings]
    )
    vulnerabilities = vulns_utils.filter_non_confirmed_zero_risk(
        all_vulnerabilities
    )

    return vulns_utils.get_mean_remediate_vulnerabilities(
        [
            vuln
            for vuln in vulnerabilities
            if not vulns_utils.is_accepted_undefined_vulnerability(vuln)
        ],
        min_date,
    )


async def get_mean_remediate_non_treated_new(
    loaders: Any, group_name: str, min_date: Optional[date] = None
) -> Decimal:
    findings: Tuple[Finding, ...] = await loaders.group_findings_new.load(
        group_name
    )
    all_vulnerabilities = await loaders.finding_vulns.load_many_chained(
        [finding.id for finding in findings]
    )
    vulnerabilities = vulns_utils.filter_non_confirmed_zero_risk(
        all_vulnerabilities
    )

    return vulns_utils.get_mean_remediate_vulnerabilities(
        [
            vuln
            for vuln in vulnerabilities
            if not vulns_utils.is_accepted_undefined_vulnerability(vuln)
        ],
        min_date,
    )


async def get_mean_remediate_severity_cvssf(
    loaders: Any,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: Optional[date] = None,
) -> Decimal:
    group_findings = await loaders.group_findings.load(group_name.lower())
    group_findings_ids = [
        finding["finding_id"]
        for finding in group_findings
        if (
            min_severity
            <= Decimal(finding.get("cvss_temporal", 0))
            <= max_severity
        )
    ]
    finding_cvssf: Dict[str, Decimal] = {
        str(finding["finding_id"]): vulns_utils.get_cvssf(
            Decimal(finding.get("cvss_temporal", 0.0))
        )
        for finding in group_findings
    }
    findings_vulns = await loaders.finding_vulns_nzr.load_many_chained(
        group_findings_ids
    )
    return vulns_utils.get_mean_remediate_vulnerabilities_cvssf(
        findings_vulns, finding_cvssf, min_date
    )


async def get_mean_remediate_severity(
    context: Any,
    group_name: str,
    min_severity: float,
    max_severity: float,
    min_date: Optional[date] = None,
) -> Decimal:
    """Get mean time to remediate"""
    finding_vulns_loader = context.finding_vulns_nzr
    group_findings_loader = context.group_findings

    group_findings = await group_findings_loader.load(group_name.lower())
    group_findings_ids = [
        finding["finding_id"]
        for finding in group_findings
        if (
            min_severity
            <= cast(float, finding.get("cvss_temporal", 0))
            <= max_severity
        )
    ]
    findings_vulns = await finding_vulns_loader.load_many_chained(
        group_findings_ids
    )
    return vulns_utils.get_mean_remediate_vulnerabilities(
        findings_vulns, min_date
    )


async def get_mean_remediate_severity_new(
    loaders: Any,
    group_name: str,
    min_severity: float,
    max_severity: float,
    min_date: Optional[date] = None,
) -> Decimal:
    """Get mean time to remediate"""
    finding_vulns_loader = loaders.finding_vulns_nzr
    group_findings_loader = loaders.group_findings_new

    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name.lower()
    )
    group_findings_ids: List[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= float(findings_domain.get_severity_score_new(finding.severity))
            <= max_severity
        )
    ]
    findings_vulns = await finding_vulns_loader.load_many_chained(
        group_findings_ids
    )
    return vulns_utils.get_mean_remediate_vulnerabilities(
        findings_vulns, min_date
    )


async def get_open_finding(context: Any, group_name: str) -> int:
    group_findings = await context.group_findings.load(group_name)
    vulns = await context.finding_vulns_nzr.load_many_chained(
        [finding["finding_id"] for finding in group_findings]
    )

    finding_vulns_dict = defaultdict(list)
    for vuln in vulns:
        finding_vulns_dict[vuln["finding_id"]].append(vuln)
    finding_vulns = list(finding_vulns_dict.values())

    return vulns_utils.get_open_findings(finding_vulns)


async def get_open_finding_new(loaders: Any, group_name: str) -> int:
    finding_vulns_loader = loaders.finding_vulns_nzr
    group_findings_loader = loaders.group_findings_new

    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    vulns = await finding_vulns_loader.load_many_chained(
        [finding.id for finding in group_findings]
    )

    finding_vulns_dict = defaultdict(list)
    for vuln in vulns:
        finding_vulns_dict[vuln["finding_id"]].append(vuln)
    finding_vulns = list(finding_vulns_dict.values())
    return vulns_utils.get_open_findings(finding_vulns)


async def get_open_vulnerabilities(context: Any, group_name: str) -> int:
    group_findings_loader = context.group_findings
    group_findings_loader.clear(group_name)
    finding_vulns_loader = context.finding_vulns_nzr

    group_findings = await group_findings_loader.load(group_name)
    findings_vulns = await finding_vulns_loader.load_many_chained(
        [finding["finding_id"] for finding in group_findings]
    )

    last_approved_status = [
        vulns_utils.get_last_status(vuln) for vuln in findings_vulns
    ]
    return last_approved_status.count("open")


async def get_open_vulnerabilities_new(
    loaders: Any,
    group_name: str,
) -> int:
    group_findings_loader = loaders.group_findings_new
    group_findings_loader.clear(group_name)
    finding_vulns_loader = loaders.finding_vulns_nzr

    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    findings_vulns = await finding_vulns_loader.load_many_chained(
        [finding.id for finding in group_findings]
    )

    last_approved_status = [
        vulns_utils.get_last_status(vuln) for vuln in findings_vulns
    ]
    return last_approved_status.count("open")


async def invite_to_group(
    email: str,
    responsibility: str,
    role: str,
    phone_number: str,
    group_name: str,
) -> bool:
    success = False
    if (
        validate_field_length(responsibility, 50)
        and validate_alphanumeric_field(responsibility)
        and validate_phone_field(phone_number)
        and validate_email_address(email)
        and await authz.validate_fluidattacks_staff_on_group(
            group_name, email, role
        )
    ):
        expiration_time = datetime_utils.get_as_epoch(
            datetime_utils.get_now_plus_delta(weeks=1)
        )
        url_token = secrets.token_urlsafe(64)
        success = await group_access_domain.update(
            email,
            group_name,
            {
                "expiration_time": expiration_time,
                "has_access": False,
                "invitation": {
                    "is_used": False,
                    "phone_number": phone_number,
                    "responsibility": responsibility,
                    "role": role,
                    "url_token": url_token,
                },
            },
        )
        description = await get_description(group_name.lower())
        group_url = f"{BASE_URL}/confirm_access/{url_token}"
        mail_to = [email]
        email_context: MailContentType = {
            "admin": email,
            "group": group_name,
            "group_description": description,
            "group_url": group_url,
        }
        schedule(groups_mail.send_mail_access_granted(mail_to, email_context))
    return success


async def is_alive(
    group: str, pre_computed_group_data: Optional[GroupType] = None
) -> bool:
    return await groups_dal.is_alive(group, pre_computed_group_data)


async def mask(group_name: str) -> bool:
    today = datetime_utils.get_now()
    are_comments_masked = await mask_comments(group_name)
    update_data: Dict[str, Union[str, List[str], object]] = {
        "project_status": "FINISHED",
        "deletion_date": datetime_utils.get_as_str(today),
    }
    is_group_finished = await update(group_name, update_data)
    return are_comments_masked and is_group_finished


async def mask_resources(group_name: str) -> NamedTuple:
    group_name = group_name.lower()
    group = await get_attributes(
        group_name, ["environments", "files", "repositories"]
    )
    status: NamedTuple = namedtuple(  # NOSONAR
        "status", ("files_result environments_result repositories_result")
    )
    list_resources_files = await resources_utils.search_file(f"{group_name}/")
    await collect(
        resources_utils.remove_file(file_name)
        for file_name in list_resources_files
    )

    files_result = await update(
        group_name,
        {
            "files": [
                {
                    "fileName": "Masked",
                    "description": "Masked",
                    "uploader": "Masked",
                }
                for _ in group.get("files", [])
            ]
        },
    )
    environments_result = await update(
        group_name,
        {
            "environments": [
                {"urlEnv": "Masked"} for _ in group.get("environments", [])
            ]
        },
    )
    repositories_result = await update(
        group_name,
        {
            "repositories": [
                {"protocol": "Masked", "urlRepo": "Masked"}
                for _ in group.get("repositories", [])
            ]
        },
    )
    return cast(
        NamedTuple,
        status(
            files_result,
            environments_result,
            repositories_result,
        ),
    )


async def remove_all_users(loaders: Any, group: str) -> bool:
    """Remove user access to group"""
    user_active, user_suspended = await collect(
        [
            group_access_domain.get_group_users(group, True),
            group_access_domain.get_group_users(group, False),
        ]
    )
    all_users = user_active + user_suspended
    return all(
        await collect(
            [remove_user(loaders, group, user) for user in all_users]
        )
    )


async def remove_resources(  # pylint: disable=too-many-locals
    loaders: Any, group_name: str
) -> bool:
    are_users_removed = await remove_all_users(loaders, group_name)
    if FI_API_STATUS == "migration":
        group_drafts_loader: DataLoader = loaders.group_drafts_new
        drafts: Tuple[Finding, ...] = await group_drafts_loader.load(
            group_name
        )
        group_all_findings_loader: DataLoader = loaders.group_findings_all_new
        all_findings: Tuple[
            Finding, ...
        ] = await group_all_findings_loader.load(group_name)
        are_findings_masked = all(
            await collect(
                findings_domain.mask_finding_new(loaders, finding)
                for finding in drafts + all_findings
            )
        )
    else:
        group_findings = await findings_domain.list_findings(
            loaders, [group_name], include_deleted=True
        )
        group_drafts = await findings_domain.list_drafts(
            [group_name], include_deleted=True
        )
        findings_and_drafts = group_findings[0] + group_drafts[0]
        are_findings_masked = all(
            await collect(
                findings_domain.mask_finding(loaders, finding_id)
                for finding_id in findings_and_drafts
            )
        )
    events = await events_domain.list_group_events(group_name)
    are_events_masked = all(
        await collect(events_domain.mask(event_id) for event_id in events)
    )
    is_group_masked = await mask(group_name)
    are_resources_masked = all(
        list(cast(List[bool], await mask_resources(group_name)))
    )
    return all(
        [
            are_findings_masked,
            are_users_removed,
            is_group_masked,
            are_events_masked,
            are_resources_masked,
        ]
    )


async def remove_user(
    loaders: Any, group_name: str, email: str, check_org_access: bool = True
) -> bool:
    """Remove user access to group"""
    success: bool = await group_access_domain.remove_access(email, group_name)
    if success and check_org_access:
        group_loader = loaders.group
        group = await group_loader.load(group_name)
        org_id = group["organization"]

        has_org_access = await orgs_domain.has_user_access(org_id, email)
        has_groups_in_org = bool(
            await get_groups_by_user(email, organization_id=org_id)
        )
        if has_org_access and not has_groups_in_org:
            success = success and await orgs_domain.remove_user(org_id, email)

        has_groups = bool(await get_groups_by_user(email))
        if not has_groups:
            success = success and await users_domain.delete(email)
    return success


async def update(group_name: str, data: GroupType) -> bool:
    return await groups_dal.update(group_name, data)


async def update_pending_deletion_date(
    group_name: str, pending_deletion_date: Optional[str]
) -> bool:
    """Update pending deletion date"""
    values: GroupType = {"pending_deletion_date": pending_deletion_date}
    success = await update(group_name, values)
    return success


async def update_tags(
    group_name: str, group_tags: GroupType, tags: List[str]
) -> bool:
    success: bool = False
    if not group_tags["tag"]:
        group_tags = {"tag": set(tags)}
    else:
        cast(Set[str], group_tags.get("tag")).update(tags)
    success = await update(group_name, group_tags)
    if not success:
        LOGGER.error("Couldn't add tags", extra={"extra": locals()})
    return success


def validate_group_services_config(
    has_machine: bool,
    has_squad: bool,
    has_asm: bool,
) -> None:
    if has_squad:
        if not has_asm:
            raise InvalidGroupServicesConfig(
                "Squad is only available when ASM is too"
            )
        if not has_machine:
            raise InvalidGroupServicesConfig(
                "Squad is only available when Machine is too"
            )


async def validate_group_tags(group_name: str, tags: List[str]) -> List[str]:
    """Validate tags array"""
    pattern = re.compile("^[a-z0-9]+(?:-[a-z0-9]+)*$")
    if await _has_repeated_tags(group_name, tags):
        raise RepeatedValues()
    return [tag for tag in tags if pattern.match(tag)]


async def after_complete_register(group_access: GroupAccessType) -> None:
    group_name: str = str(get_key_or_fallback(group_access))
    user_email: str = str(group_access["user_email"])
    enforcer = await authz.get_user_level_enforcer(user_email)
    if enforcer("self", "keep_default_organization_access"):
        return
    organization_id: str = await orgs_domain.get_id_for_group(group_name)
    default_org = await orgs_domain.get_or_add(FI_DEFAULT_ORG)
    default_org_id: str = str(default_org["id"])
    if (
        organization_id != default_org_id
        and await orgs_domain.has_user_access(default_org_id, user_email)
    ):
        await orgs_domain.remove_user(default_org_id, user_email)


def filter_active_groups(groups: List[GroupType]) -> List[GroupType]:
    return [
        group
        for group in groups
        if get_key_or_fallback(group, "group_status", "project_status")
        == "ACTIVE"
    ]


async def get_remediation_rate(
    context: Any,
    group_name: str,
) -> int:
    """Percentage of closed vulns, ignoring treatments"""
    remediation_rate: int = 0
    open_vulns = await get_open_vulnerabilities(context, group_name)
    closed_vulns = await get_closed_vulnerabilities(context, group_name)
    if closed_vulns:
        remediation_rate = int(
            100 * closed_vulns / (open_vulns + closed_vulns)
        )
    return remediation_rate


async def get_remediation_rate_new(
    loaders: Any,
    group_name: str,
) -> int:
    """Percentage of closed vulns, ignoring treatments"""
    remediation_rate: int = 0
    open_vulns = await get_open_vulnerabilities_new(loaders, group_name)
    closed_vulns = await get_closed_vulnerabilities_new(loaders, group_name)
    if closed_vulns:
        remediation_rate = int(
            100 * closed_vulns / (open_vulns + closed_vulns)
        )
    return remediation_rate


async def get_group_digest_stats(  # pylint: disable=too-many-locals
    loaders: Any, group_name: str
) -> MailContentType:
    content: MailContentType = {
        "group": group_name,
        "main": {
            "group_age": 0,
            "remediation_rate": 0,
            "remediation_time": 0,
            "comments": 0,
        },
        "reattacks": {
            "effective_reattacks": 0,
            "effective_reattacks_total": 0,
            "reattacks_requested": 0,
            "last_requested_date": "",
            "reattacks_executed": 0,
            "reattacks_executed_total": 0,
            "last_executed_date": "",
            "pending_attacks": 0,
        },
        "treatments": {
            "temporary_applied": 0,
            "eternal_requested": 0,
            "eternal_approved": 0,
        },
        "events": {
            "unsolved": 0,
            "new": 0,
        },
        "findings": list(),
        "vulns_len": 0,
    }

    if FI_API_STATUS == "migration":
        findings_loader = loaders.group_findings_new
        findings: Tuple[Finding, ...] = await findings_loader.load(group_name)
        findings_ids = [finding.id for finding in findings]
    else:
        findings_loader = loaders.group_findings
        findings = await findings_loader.load(group_name)
        findings_ids = [str(finding["finding_id"]) for finding in findings]

    finding_vulns_loader = loaders.finding_vulns_nzr
    group_vulns = await finding_vulns_loader.load_many_chained(findings_ids)

    if len(group_vulns) == 0:
        LOGGER_CONSOLE.info(f"NO vulns at {group_name}", **NOEXTRA)
        return content

    content["vulns_len"] = len(group_vulns)
    last_day = datetime_utils.get_now_minus_delta(hours=24)

    if FI_API_STATUS == "migration":
        oldest_finding = await get_oldest_no_treatment_new(loaders, findings)
        if oldest_finding:
            max_severity, severest_finding = await get_max_open_severity_new(
                loaders, findings
            )
            content["findings"] = [
                {
                    **oldest_finding,
                    "severest_name": severest_finding.title
                    if severest_finding
                    else "",
                    "severity": str(max_severity),
                }
            ]
        content["main"]["remediation_time"] = int(
            await get_mean_remediate_non_treated_new(loaders, group_name)
        )
        content["main"]["remediation_rate"] = await get_remediation_rate_new(
            loaders, group_name
        )
    else:
        oldest_finding = await get_oldest_no_treatment(loaders, findings)
        if oldest_finding:
            max_severity, severest_finding = await get_max_open_severity(
                loaders, findings
            )
            content["findings"] = [
                {
                    **oldest_finding,
                    "severest_name": severest_finding.get("finding", ""),
                    "severity": str(max_severity),
                }
            ]
        content["main"]["remediation_time"] = int(
            await get_mean_remediate_non_treated(loaders, group_name)
        )
        content["main"]["remediation_rate"] = await get_remediation_rate(
            loaders, group_name
        )

    historic_config = (
        await get_attributes(group_name, ["historic_configuration"])
    )["historic_configuration"]
    historic_config_date = datetime_utils.get_from_str(
        cast(HistoricType, historic_config)[0]["date"]
    )
    group_age = (datetime_utils.get_now() - historic_config_date).days
    content["main"]["group_age"] = group_age
    treatments = await vulns_utils.get_total_treatment_date(
        group_vulns, last_day
    )
    content["treatments"]["temporary_applied"] = treatments.get("accepted", 0)
    content["treatments"]["eternal_requested"] = treatments.get(
        "accepted_undefined_submitted", 0
    )
    content["treatments"]["eternal_approved"] = treatments.get(
        "accepted_undefined_approved", 0
    )
    content["reattacks"] = await vulns_utils.get_total_reattacks_stats(
        group_vulns, last_day
    )
    content["main"]["comments"] = await get_total_comments_date(
        findings_ids, group_name, last_day
    )
    unsolved = await events_domain.get_unsolved_events(group_name)
    new_events = await events_utils.filter_events_date(unsolved, last_day)
    content["events"]["unsolved"] = len(unsolved)
    content["events"]["new"] = len(new_events)

    return content


def process_user_digest_stats(
    group_stats_all: Tuple[MailContentType],
) -> MailContentType:
    """Consolidate several groups stats with precalculated data"""
    # Filter out those groups with no vulns
    groups_stats: Tuple[MailContentType] = cast(
        Tuple[MailContentType],
        tuple(group for group in group_stats_all if group["vulns_len"] > 0),
    )

    if len(groups_stats) == 0:
        return {
            "groups_len": 0,
        }

    total: MailContentType = {
        "groups_len": len(groups_stats),
        "group_age": {
            "oldest_age": 0,
            "oldest_group": groups_stats[0]["group"],
            "youngest_age": groups_stats[0]["main"]["group_age"],
            "newest_group": groups_stats[0]["group"],
        },
        "remediation_rate": {
            "max": 0,
            "max_group": groups_stats[0]["group"],
            "min": groups_stats[0]["main"]["remediation_rate"],
            "min_group": groups_stats[0]["group"],
        },
        "remediation_time": {
            "max": 0,
            "max_group": groups_stats[0]["group"],
            "min": groups_stats[0]["main"]["remediation_time"],
            "min_group": groups_stats[0]["group"],
        },
        "findings": list(),
    }

    main: Counter = Counter()
    treatments: Counter = Counter()
    events: Counter = Counter()
    for stat in groups_stats:
        main.update(stat["main"])
        treatments.update(stat["treatments"])
        events.update(stat["events"])
        # Get highest among groups
        if stat["main"]["group_age"] > total["group_age"]["oldest_age"]:
            total["group_age"]["oldest_age"] = stat["main"]["group_age"]
            total["group_age"]["oldest_group"] = stat["group"]
        if stat["main"]["remediation_rate"] > total["remediation_rate"]["max"]:
            total["remediation_rate"]["max"] = stat["main"]["remediation_rate"]
            total["remediation_rate"]["max_group"] = stat["group"]
        if stat["main"]["remediation_time"] > total["remediation_time"]["max"]:
            total["remediation_time"]["max"] = stat["main"]["remediation_time"]
            total["remediation_time"]["max_group"] = stat["group"]
        # Get lowest among groups
        if stat["main"]["group_age"] < total["group_age"]["youngest_age"]:
            total["group_age"]["youngest_age"] = stat["main"]["group_age"]
            total["group_age"]["newest_group"] = stat["group"]
        if stat["main"]["remediation_rate"] < total["remediation_rate"]["min"]:
            total["remediation_rate"]["min"] = stat["main"]["remediation_rate"]
            total["remediation_rate"]["min_group"] = stat["group"]
        if stat["main"]["remediation_time"] < total["remediation_time"]["min"]:
            total["remediation_time"]["min"] = stat["main"]["remediation_time"]
            total["remediation_time"]["min_group"] = stat["group"]

    total["main"] = dict(main)
    total["events"] = dict(events)

    total["reattacks"] = _process_digest_reattacks(groups_stats)
    total["treatments"] = _process_digest_treatments(groups_stats)

    # Get top 10 findings that have oldest vulns without treatment
    findings = list()
    for stat in groups_stats:
        findings_extended = [
            {
                **finding,
                "finding_group": stat["group"],
            }
            for finding in stat["findings"]
        ]
        findings.extend(findings_extended)
    total["findings"] = sorted(
        findings, key=itemgetter("oldest_age"), reverse=True
    )[:10]

    return total
