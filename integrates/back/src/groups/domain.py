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
import bugsnag
from collections import (
    Counter,
)
from context import (
    BASE_URL,
    FI_DEFAULT_ORG,
    FI_ENVIRONMENT,
)
from contextlib import (
    AsyncExitStack,
)
from custom_exceptions import (
    AlreadyPendingDeletion,
    BillingSubscriptionSameActive,
    ErrorRemovingGroup,
    ErrorUpdatingGroup,
    GroupNotFound,
    HasActiveRoots,
    InvalidGroupName,
    InvalidGroupServicesConfig,
    InvalidGroupTier,
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
from db_model.groups.constants import (
    MASKED,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupService,
    GroupStateRemovalJustification,
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
)
from db_model.roots.types import (
    RootItem,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)
from dynamodb.operations_legacy import (
    start_context,
)
from events import (
    domain as events_domain,
)
from findings import (
    domain as findings_domain,
)
from findings.domain import (
    get_max_open_severity,
    get_oldest_no_treatment,
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
    datetime as datetime_utils,
    events as events_utils,
    groups as groups_utils,
    resources as resources_utils,
    validations,
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
    reattacks_requested: int, groups_stats: Tuple[MailContentType, ...]
) -> MailContentType:
    """Process digest reattacks requested sub-section"""
    requested: MailContentType = {
        "groups_requested": [],
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
        )
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
        )

    return requested


def _process_digest_reattacks_executed(
    reattacks_executed: int,
    reattacks_executed_total: int,
    effective_reattacks_total: int,
    groups_stats: Tuple[MailContentType, ...],
) -> MailContentType:
    """Process digest reattacks executed sub-section"""
    executed: MailContentType = {
        "groups_executed": [],
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
        )
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
        )

    # Also known as "remediation effectiveness"
    if reattacks_executed_total:
        executed["reattack_effectiveness"] = int(
            100 * effective_reattacks_total / reattacks_executed_total
        )

    return executed


def _process_digest_reattacks_pending(
    groups_stats: Tuple[MailContentType, ...],
) -> MailContentType:
    """Process digest pending reattacks sub-section"""
    pending: MailContentType = {
        "groups_pending": [],
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
    )

    return pending


def _process_digest_reattacks(
    groups_stats: Tuple[MailContentType, ...],
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
    groups_stats: Tuple[MailContentType, ...],
) -> MailContentType:
    """Process digest treatments section"""
    treatments_count: Counter = Counter()
    for stat in groups_stats:
        treatments_count.update(stat["treatments"])
    treatments = dict(treatments_count)

    # Get groups with most temporary applied
    temporary: MailContentType = {
        "groups_temporary": [],
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
    )
    treatments.update(temporary)

    # Get groups with most permanent requested
    permanent_requested: MailContentType = {
        "groups_permanent_requested": [],
    }
    groups_permanent_requested = [
        {
            "permanent_requested": group["treatments"]["permanent_requested"],
            "group": group["group"],
        }
        for group in groups_stats
        if group["treatments"]["permanent_requested"]
    ]
    permanent_requested["groups_permanent_requested"] = sorted(
        groups_permanent_requested,
        key=itemgetter("permanent_requested"),
        reverse=True,
    )
    treatments.update(permanent_requested)

    # Get groups with most permanent approved
    permanent_approved: MailContentType = {
        "groups_permanent_approved": [],
    }
    groups_permanent_approved = [
        {
            "permanent_approved": group["treatments"]["permanent_approved"],
            "group": group["group"],
        }
        for group in groups_stats
        if group["treatments"]["permanent_approved"]
    ]
    permanent_approved["groups_permanent_approved"] = sorted(
        groups_permanent_approved,
        key=itemgetter("permanent_approved"),
        reverse=True,
    )
    treatments.update(permanent_approved)

    # Get groups with most undefined
    undefined: MailContentType = {
        "groups_undefined": [],
    }
    groups_undefined = [
        {
            "undefined": group["treatments"]["undefined"],
            "group": group["group"],
        }
        for group in groups_stats
        if group["treatments"]["undefined"]
    ]
    undefined["groups_undefined"] = sorted(
        groups_undefined,
        key=itemgetter("undefined"),
        reverse=True,
    )
    treatments.update(undefined)

    return treatments


async def _has_repeated_tags(group_name: str, tags: List[str]) -> bool:
    has_repeated_tags = len(tags) != len(set(tags))
    if not has_repeated_tags:
        group_info = await get_attributes(group_name.lower(), ["tag"])
        existing_tags = group_info.get("tag", [])
        all_tags = list(existing_tags) + tags
        has_repeated_tags = len(all_tags) != len(set(all_tags))
    return has_repeated_tags


async def complete_register_for_group_invitation(
    group_access: GroupAccessType,
) -> bool:
    coroutines: List[Awaitable[bool]] = []
    success: bool = False
    invitation = cast(InvitationType, group_access["invitation"])
    if invitation["is_used"]:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    group_name = cast(str, get_key_or_fallback(group_access))
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
            orgs_domain.add_user(organization_id, user_email, "user")
        )

    if not await users_domain.is_registered(user_email):
        coroutines.extend(
            [
                users_domain.register(user_email),
                authz.grant_user_level_role(user_email, "user"),
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


async def complete_register_for_organization_invitation(
    organization_access: Dict[str, Any]
) -> bool:
    success: bool = False
    invitation = organization_access["invitation"]
    if invitation["is_used"]:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    organization_id = organization_access["pk"]
    organization_name = await orgs_domain.get_name_by_id(organization_id)
    role = invitation["role"]
    user_email = organization_access["sk"].split("#")[1]
    updated_invitation = invitation.copy()
    updated_invitation["is_used"] = True

    user_added = await orgs_domain.add_user(organization_id, user_email, role)

    await orgs_domain.update(
        organization_id,
        user_email,
        {
            "expiration_time": None,
            "has_access": True,
            "invitation": updated_invitation,
        },
    )

    user_created = False
    user_exists = bool(await users_domain.get_data(user_email, "email"))
    if not user_exists:
        user_created = await add_without_group(
            user_email,
            "user",
            should_add_default_org=(
                FI_DEFAULT_ORG.lower() == organization_name.lower()
            ),
            is_register_after_complete=True,
        )

    success = user_added and any([user_created, user_exists])
    if success:
        redis_del_by_deps_soon(
            "confirm_access_organization",
            organization_id=organization_id,
        )
    return success


async def reject_register_for_group_invitation(
    loaders: Any,
    group_access: GroupAccessType,
) -> bool:
    success: bool = False
    invitation = cast(InvitationType, group_access["invitation"])
    if invitation["is_used"]:
        bugsnag.notify(Exception("Token already used"), severity="warning")

    group_name = cast(str, get_key_or_fallback(group_access))
    user_email = cast(str, group_access["user_email"])
    success = await group_access_domain.remove_access(
        loaders, user_email, group_name
    )

    return success


async def add_group(  # pylint: disable=too-many-locals
    *,
    description: str,
    group_name: str,
    organization_name: str,
    service: GroupService,
    user_email: str,
    user_role: str,
    has_machine: bool = False,
    has_squad: bool = False,
    language: str = GroupLanguage.EN,
    subscription: str = GroupSubscriptionType.CONTINUOUS,
    tier: str = GroupTier.FREE,
) -> None:
    validate_group_name(group_name)
    validate_fields([description])
    validate_field_length(group_name, 20)
    validate_field_length(description, 200)
    validate_group_services_config(
        has_machine,
        has_squad,
        has_asm=True,
    )

    if not description.strip() or not group_name.strip():
        raise InvalidParameter()

    org_id = await orgs_domain.get_id_by_name(organization_name)
    if not await orgs_domain.has_user_access(org_id, user_email):
        raise UserNotInOrganization(org_id)

    is_group_avail, group_exists = await collect(
        [
            names_domain.exists(group_name, "group"),
            groups_dal.exists(group_name),
        ]
    )
    if not is_group_avail or group_exists:
        raise InvalidGroupName()

    await groups_dal.add_typed(
        group=Group(
            description=description,
            language=language,
            name=group_name,
            state=GroupState(
                has_machine=has_machine,
                has_squad=has_squad,
                modified_by=user_email,
                modified_date=datetime_utils.get_iso_date(),
                service=service,
                status=GroupStateStatus.ACTIVE,
                tier=tier,
                type=subscription,
            ),
            organization_name=organization_name,
        )
    )
    await collect(
        (
            orgs_domain.add_group(org_id, group_name),
            names_domain.remove(group_name, "group"),
        )
    )

    success: bool = False
    # Admins are not granted access to the group
    # they are omnipresent
    if user_role != "admin":
        # Only Fluid staff can be customer managers
        # Customers are granted the user manager role
        role: str = (
            "customer_manager"
            if users_domain.is_fluid_staff(user_email)
            else "user_manager"
        )
        success = all(
            await collect(
                (
                    group_access_domain.update_has_access(
                        user_email, group_name, True
                    ),
                    authz.grant_group_level_role(user_email, group_name, role),
                )
            )
        )

    # Notify us in case the user wants any Fluid Service
    if success:
        await notifications_domain.new_group(
            description=description,
            group_name=group_name,
            has_machine=has_machine,
            has_squad=has_squad,
            organization=organization_name,
            requester_email=user_email,
            service=service,
            subscription=subscription,
        )


async def add_without_group(
    email: str,
    role: str,
    should_add_default_org: bool = True,
    is_register_after_complete: bool = False,
) -> bool:
    success = False
    if validate_email_address(email):
        new_user_data: UserType = {}
        new_user_data["email"] = email
        if is_register_after_complete:
            new_user_data["registered"] = True

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
            await orgs_domain.add_user(str(org["id"]), email, "user")
    return success


async def deactivate_all_roots(
    loaders: Any,
    group_name: str,
    user_email: str,
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
                user_email=user_email,
            )
            for root in all_group_roots
        ]
    )


async def remove_group(
    loaders: Any,
    group_name: str,
    user_email: str,
    organization_id: str,
    reason: Optional[str] = "",
) -> bool:
    """
    Update group state to DELETED and update some related resources.
    For production, remember to remove additional resources
    (user, findings, vulns ,etc) via the batch action remove_group_resources.
    """
    data = await groups_dal.get_attributes(
        group_name, ["project_status", "historic_deletion"]
    )
    if (
        get_key_or_fallback(data, "group_status", "project_status")
        == "DELETED"
    ):
        raise AlreadyPendingDeletion()

    all_resources_removed = True
    if FI_ENVIRONMENT == "development":
        all_resources_removed = await remove_resources(
            loaders=loaders, group_name=group_name, user_email=user_email
        )
    are_users_removed = await remove_all_users(
        loaders=loaders, group_name=group_name
    )
    are_policies_revoked = await authz.revoke_cached_group_service_policies(
        group_name
    )
    is_removed_from_org = await orgs_domain.remove_group(
        group_name, organization_id
    )
    if not all(
        [
            are_users_removed,
            all_resources_removed,
            are_policies_revoked,
            is_removed_from_org,
        ]
    ):
        return False

    today = datetime_utils.get_now_as_str()
    new_state = {
        "date": today,
        "deletion_date": today,
        "user": user_email.lower(),
    }
    historic_deletion = cast(
        List[Dict[str, str]], data.get("historic_deletion", [])
    )
    historic_deletion.append(new_state)
    new_data: GroupType = {
        "historic_deletion": historic_deletion,
        "group_status": "DELETED",
        "project_status": "DELETED",
        "reason": reason,
        "deletion_date": today,
    }
    return await update(group_name, new_data)


async def remove_group_typed(
    *,
    loaders: Any,
    group_name: str,
    justification: GroupStateRemovalJustification,
    user_email: str,
) -> None:
    """
    Update group state to DELETED and update some related resources.
    For production, remember to remove additional resources
    (user, findings, vulns ,etc) via the batch action remove_group_resources.
    """
    loaders.group_typed.clear(group_name)
    group: Group = await loaders.group_typed.load(group_name)
    if group.state.status == GroupStateStatus.DELETED:
        raise AlreadyPendingDeletion()

    all_resources_removed = True
    if FI_ENVIRONMENT == "development":
        all_resources_removed = await remove_resources(
            loaders=loaders,
            group_name=group_name,
            user_email=user_email,
        )
    are_users_removed = await remove_all_users(
        loaders=loaders,
        group_name=group_name,
    )
    are_policies_revoked = await authz.revoke_cached_group_service_policies(
        group_name
    )
    is_removed_from_org = await orgs_domain.remove_group(
        group_name=group_name,
        organization_id=await orgs_domain.get_id_for_group(group_name),
    )
    if not all(
        [
            are_users_removed,
            all_resources_removed,
            are_policies_revoked,
            is_removed_from_org,
        ]
    ):
        raise ErrorRemovingGroup.new()

    await update_state_typed(
        group_name=group_name,
        state=group.state._replace(
            modified_date=datetime_utils.get_iso_date(),
            has_machine=False,
            has_squad=False,
            justification=justification,
            modified_by=user_email,
            status=GroupStateStatus.DELETED,
        ),
    )


async def validate_open_roots(loaders: Any, group_name: str) -> None:
    roots: Tuple[RootItem, ...] = await loaders.group_roots.load(group_name)
    if next((root for root in roots if root.state.status == "ACTIVE"), None):
        raise HasActiveRoots()


async def update_group(
    *,
    loaders: Any,
    comments: str,
    group_name: str,
    has_asm: bool,
    has_machine: bool,
    has_squad: bool,
    justification: GroupStatusJustification,
    service: Optional[GroupService],
    subscription: GroupSubscriptionType,
    tier: GroupTier = GroupTier.OTHER,
    user_email: str,
) -> None:
    validate_fields([comments])
    validate_string_length_between(comments, 0, 250)
    validate_group_services_config(
        has_machine,
        has_squad,
        has_asm,
    )

    group: Group = await loaders.group_typed.load(group_name)
    if service != group.state.service:
        await deactivate_all_roots(
            loaders=loaders,
            group_name=group_name,
            user_email=user_email,
            other=comments,
            reason=justification.value,
        )
    if tier == GroupTier.OTHER:
        tier = GroupTier.FREE

    await update_state_typed(
        group_name=group_name,
        state=GroupState(
            comments=comments,
            modified_date=datetime_utils.get_iso_date(),
            has_machine=has_machine,
            has_squad=has_squad,
            justification=justification,
            modified_by=user_email,
            service=service,
            status=GroupStateStatus.ACTIVE,
            tier=tier,
            type=subscription,
        ),
    )
    if has_asm:
        await notifications_domain.update_group(
            comments=comments,
            group_name=group_name,
            had_asm=True,
            had_machine=group.state.has_machine,
            had_squad=group.state.has_squad,
            has_asm=has_asm,
            has_machine=has_machine,
            has_squad=has_squad,
            reason=justification.value,
            requester_email=user_email,
            service=service.value if service else "",
            subscription=str(subscription.value).lower(),
        )
        return

    org_id = await orgs_domain.get_id_for_group(group_name)
    success = await remove_group(
        loaders=loaders,
        group_name=group_name,
        user_email=user_email,
        organization_id=org_id,
        reason=justification.value,
    )
    if success:
        await notifications_domain.delete_group(
            deletion_date=datetime_utils.get_now_as_str(),
            group_name=group_name,
            requester_email=user_email,
            reason=justification.value,
        )


async def update_group_tier(
    *,
    loaders: Any,
    comments: str,
    group_name: str,
    tier: GroupTier,
    user_email: str,
) -> None:
    """Set a new tier for a group."""
    data = {
        "loaders": loaders,
        "comments": comments,
        "group_name": group_name,
        "has_asm": True,
        "has_machine": False,
        "has_squad": False,
        "justification": GroupStateUpdationJustification.OTHER,
        "service": GroupService.WHITE,
        "subscription": GroupSubscriptionType.CONTINUOUS,
        "tier": tier,
        "user_email": user_email,
    }

    if tier == GroupTier.MACHINE:
        data["subscription"] = GroupSubscriptionType.CONTINUOUS
        data["has_machine"] = True
        data["has_squad"] = False
        data["service"] = GroupService.WHITE
    elif tier == GroupTier.SQUAD:
        data["subscription"] = GroupSubscriptionType.CONTINUOUS
        data["has_machine"] = True
        data["has_squad"] = True
        data["service"] = GroupService.WHITE
    elif tier == GroupTier.ONESHOT:
        data["subscription"] = GroupSubscriptionType.ONESHOT
        data["has_machine"] = False
        data["has_squad"] = False
        data["service"] = GroupService.BLACK
    elif tier == GroupTier.FREE:
        data["subscription"] = GroupSubscriptionType.CONTINUOUS
        data["has_machine"] = False
        data["has_squad"] = False
        data["service"] = GroupService.WHITE
    else:
        raise InvalidGroupTier()

    await update_group(**data)


async def get_active_groups() -> List[str]:
    groups = await groups_dal.get_active_groups()
    return groups


async def get_all(attributes: Optional[List[str]] = None) -> List[GroupType]:
    data_attr = ",".join(attributes or [])
    return await groups_dal.get_all(data_attr=data_attr)


async def get_active_groups_attributes(
    attributes: Optional[List[str]] = None,
) -> List[GroupType]:
    data_attr = ",".join(attributes or [])
    groups = await groups_dal.get_active_groups_attributes(data_attr)
    return groups


async def get_attributes(
    group_name: str, attributes: List[str]
) -> Dict[str, Union[str, List[str]]]:
    return await groups_dal.get_attributes(group_name, attributes)


async def get_closed_vulnerabilities(loaders: Any, group_name: str) -> int:
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    findings_vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in group_findings]
    )

    last_approved_status = [vuln.state.status for vuln in findings_vulns]
    return last_approved_status.count(VulnerabilityStateStatus.CLOSED)


async def get_group_info(group_name: str) -> Tuple[str, str, str]:
    """Returns the description, business_id, and business_name attrs
    of a Group"""
    return await groups_dal.get_group_info(group_name)


async def get_groups_by_user(
    user_email: str,
    active: bool = True,
    organization_id: str = "",
    with_cache: bool = True,
) -> List[str]:
    user_groups: List[str] = []
    groups = await group_access_domain.get_user_groups(user_email, active)
    group_level_roles = await authz.get_group_level_roles(
        user_email, groups, with_cache=with_cache
    )
    if organization_id:
        org_groups: Set[str] = set(
            await orgs_domain.get_groups(organization_id)
        )
        groups = [group for group in groups if group in org_groups]

    user_groups = [
        group
        for role, group in zip(group_level_roles.values(), groups)
        if bool(role)
    ]

    return user_groups


async def get_vulnerabilities_with_pending_attacks(
    *,
    loaders: Any,
    group_name: str,
) -> int:
    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    vulnerabilities: Tuple[
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


async def get_groups_with_forces() -> List[str]:
    return await groups_dal.get_groups_with_forces()


async def get_many_groups(groups_name: List[str]) -> List[GroupType]:
    async with AsyncExitStack() as stack:
        resource = await stack.enter_async_context(start_context())
        table = await resource.Table(groups_dal.TABLE_NAME)
        groups = await collect(
            tuple(
                groups_dal.get_group(group_name, table)
                for group_name in groups_name
            )
        )
    return cast(List[GroupType], groups)


async def get_mean_remediate_severity_cvssf(
    loaders: Any,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: Optional[date] = None,
) -> Decimal:
    group_findings_loader = loaders.group_findings
    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name.lower()
    )
    group_findings_ids: List[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= findings_domain.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    finding_cvssf: Dict[str, Decimal] = {
        finding.id: vulns_utils.get_cvssf(
            findings_domain.get_severity_score(finding.severity)
        )
        for finding in group_findings
    }
    findings_vulns: Tuple[
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
    loaders: Any,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: Optional[date] = None,
) -> Decimal:
    group_findings_loader = loaders.group_findings
    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name.lower()
    )
    group_findings_ids: List[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= findings_domain.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    finding_cvssf: Dict[str, Decimal] = {
        finding.id: vulns_utils.get_cvssf(
            findings_domain.get_severity_score(finding.severity)
        )
        for finding in group_findings
    }
    findings_vulns: Tuple[
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
    loaders: Any,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: Optional[date] = None,
) -> Decimal:
    """Get mean time to remediate"""
    group_findings_loader = loaders.group_findings

    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name.lower()
    )
    group_findings_ids: List[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= findings_domain.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    findings_vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities.load_many_chained(
        group_findings_ids
    )
    return vulns_utils.get_mean_remediate_vulnerabilities(
        findings_vulns,
        min_date,
    )


async def get_mean_remediate_non_treated_severity(
    loaders: Any,
    group_name: str,
    min_severity: Decimal,
    max_severity: Decimal,
    min_date: Optional[date] = None,
) -> Decimal:
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name.lower()
    )
    group_findings_ids: List[str] = [
        finding.id
        for finding in group_findings
        if (
            min_severity
            <= findings_domain.get_severity_score(finding.severity)
            <= max_severity
        )
    ]
    findings_vulns: Tuple[
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


async def get_open_findings(loaders: Any, group_name: str) -> int:
    group_findings_loader = loaders.group_findings
    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
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
    loaders: Any,
    group_name: str,
) -> int:
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    findings_vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        [finding.id for finding in group_findings]
    )

    last_approved_status = [vuln.state.status for vuln in findings_vulns]
    return last_approved_status.count(VulnerabilityStateStatus.OPEN)


async def invite_to_group(
    *,
    loaders: Any,
    email: str,
    responsibility: str,
    role: str,
    group_name: str,
    modified_by: str,
) -> bool:
    success = False
    if (
        validate_field_length(responsibility, 50)
        and validate_alphanumeric_field(responsibility)
        and validate_email_address(email)
        and validate_role_fluid_reqs(email, role)
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
                    "responsibility": responsibility,
                    "role": role,
                    "url_token": url_token,
                },
            },
        )
        group: Group = await loaders.group_typed.load(group_name)
        confirm_access_url = f"{BASE_URL}/confirm_access/{url_token}"
        reject_access_url = f"{BASE_URL}/reject_access/{url_token}"
        mail_to = [email]
        email_context: MailContentType = {
            "admin": email,
            "group": group_name,
            "responsible": modified_by,
            "group_description": group.description,
            "confirm_access_url": confirm_access_url,
            "reject_access_url": reject_access_url,
        }
        schedule(groups_mail.send_mail_access_granted(mail_to, email_context))
    return success


async def is_valid(
    group: str, pre_computed_group_data: Optional[GroupType] = None
) -> bool:
    return await groups_dal.is_valid(group, pre_computed_group_data)


async def mask_files(
    loaders: Any,
    group_name: str,
) -> None:
    group: Group = await loaders.group_typed.load(group_name)
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
        await update_metadata_typed(
            group_name=group_name,
            metadata=GroupMetadataToUpdate(files=masked_files),
        )


async def add_file(
    *,
    loaders: Any,
    description: str,
    file_name: str,
    group_name: str,
    user_email: str,
) -> None:
    group: Group = await loaders.group_typed.load(group_name)
    validations.validate_fields([description])
    validations.validate_field_length(description, 200)
    validations.validate_file_name(file_name)
    validations.validate_file_exists(file_name, group.files)
    group_file_to_add = GroupFile(
        description=description,
        file_name=file_name,
        modified_by=user_email,
        modified_date=datetime_utils.get_iso_date(),
    )
    if not group.files:
        files_to_update: list[GroupFile] = []
    else:
        files_to_update = group.files
    files_to_update.append(group_file_to_add)
    await update_metadata_typed(
        group_name=group_name,
        metadata=GroupMetadataToUpdate(
            files=files_to_update,
        ),
    )


async def remove_file(
    *,
    loaders: Any,
    group_name: str,
    file_name: str,
) -> None:
    group: Group = await loaders.group_typed.load(group_name)
    if not group.files:
        raise ErrorUpdatingGroup.new()

    file_to_remove: Optional[GroupFile] = next(
        (file for file in group.files if file.file_name == file_name), None
    )
    if not file_to_remove:
        raise ErrorUpdatingGroup.new()

    file_url = f"{group_name}/{file_name}"
    await resources_utils.remove_file(file_url)
    await update_metadata_typed(
        group_name=group_name,
        metadata=GroupMetadataToUpdate(
            files=[
                file
                for file in group.files
                if file.file_name != file_to_remove.file_name
            ]
        ),
    )


async def remove_all_users(
    *,
    loaders: Any,
    group_name: str,
) -> bool:
    """Remove user access to group."""
    user_active, user_suspended = await collect(
        [
            group_access_domain.get_group_users(group_name, True),
            group_access_domain.get_group_users(group_name, False),
        ]
    )
    all_users = user_active + user_suspended
    return all(
        await collect(
            [remove_user(loaders, group_name, user) for user in all_users]
        )
    )


async def remove_resources(
    *,
    loaders: Any,
    group_name: str,
    user_email: str,
) -> bool:
    all_findings = await loaders.group_drafts_and_findings.load(group_name)
    are_findings_masked = all(
        await collect(
            tuple(
                findings_domain.mask_finding(loaders, finding)
                for finding in all_findings
            ),
            workers=4,
        )
    )
    events = await events_domain.list_group_events(group_name)
    are_events_masked = all(
        await collect(events_domain.mask(event_id) for event_id in events)
    )
    are_comments_masked = await mask_comments(group_name)
    await mask_files(loaders, group_name)
    await deactivate_all_roots(
        loaders=loaders,
        group_name=group_name,
        user_email=user_email,
        other="",
        reason="GROUP_DELETED",
    )
    return all(
        [
            are_findings_masked,
            are_events_masked,
            are_comments_masked,
        ]
    )


async def remove_user(
    loaders: Any,
    group_name: str,
    email: str,
) -> bool:
    """Remove user access to group."""
    success: bool = await group_access_domain.remove_access(
        loaders, email, group_name
    )
    if not success:
        return False

    group: Group = await loaders.group_typed.load(group_name)
    org_id: str = await orgs_domain.get_id_by_name(group.organization_name)

    has_org_access, user_groups_names = await collect(
        (
            orgs_domain.has_user_access(org_id, email),
            get_groups_by_user(email),
        )
    )
    org_groups_names: set[str] = set(await orgs_domain.get_groups(org_id))
    user_org_groups_names: tuple[str, ...] = tuple(
        group_name
        for group_name in user_groups_names
        if group_name in org_groups_names
    )
    user_org_groups: tuple[Group, ...] = await loaders.group_typed.load_many(
        user_org_groups_names
    )
    has_groups_in_org = bool(
        groups_utils.filter_active_groups(user_org_groups)
    )
    if has_org_access and not has_groups_in_org:
        success = await orgs_domain.remove_user(loaders, org_id, email)

    if not success:
        return False

    all_groups_by_user = await loaders.group_typed.load_many(user_groups_names)
    all_active_groups_by_user = groups_utils.filter_active_groups(
        all_groups_by_user
    )
    has_groups_in_asm = bool(all_active_groups_by_user)
    if not has_groups_in_asm:
        success = await users_domain.delete(email)
    return success


async def update(group_name: str, data: GroupType) -> bool:
    return await groups_dal.update(group_name, data)


async def update_metadata_typed(
    *,
    group_name: str,
    metadata: GroupMetadataToUpdate,
) -> None:
    await groups_dal.update_metadata_typed(
        group_name=group_name, metadata=metadata
    )


async def update_state_typed(
    *,
    group_name: str,
    state: GroupState,
) -> None:
    await groups_dal.update_state_typed(group_name=group_name, state=state)


async def update_pending_deletion_date(
    group_name: str, pending_deletion_date: Optional[str]
) -> bool:
    """Update pending deletion date"""
    values: GroupType = {"pending_deletion_date": pending_deletion_date}
    success = await update(group_name, values)
    return success


async def set_pending_deletion_date(
    group: Group,
    modified_by: str,
    pending_deletion_date: str,
) -> None:
    """Update pending deletion date in group's state."""
    await update_state_typed(
        group_name=group.name,
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
    await update_state_typed(
        group_name=group.name,
        state=group.state._replace(
            modified_by=modified_by,
            modified_date=datetime_utils.get_iso_date(),
            pending_deletion_date="",
        ),
    )


async def add_tags(
    group: Group,
    tags_to_add: set[str],
) -> None:
    updated_tags = group.tags.union(tags_to_add) if group.tags else tags_to_add
    await update_metadata_typed(
        group_name=group.name,
        metadata=GroupMetadataToUpdate(
            tags=updated_tags,
        ),
    )


async def remove_tag(
    group: Group,
    tag_to_remove: str,
) -> None:
    group.tags.remove(tag_to_remove)
    await update_metadata_typed(
        group_name=group.name,
        metadata=GroupMetadataToUpdate(
            tags=group.tags,
        ),
    )


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


async def validate_group_tags(group_name: str, tags: list[str]) -> list[str]:
    """Validate tags array."""
    pattern = re.compile("^[a-z0-9]+(?:-[a-z0-9]+)*$")
    if await _has_repeated_tags(group_name, tags):
        raise RepeatedValues()
    return [tag for tag in tags if pattern.match(tag)]


async def after_complete_register(
    loaders: Any, group_access: GroupAccessType
) -> None:
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
        await orgs_domain.remove_user(loaders, default_org_id, user_email)


async def get_remediation_rate(
    loaders: Any,
    group_name: str,
) -> int:
    """Percentage of closed vulns, ignoring treatments."""
    remediation_rate: int = 0
    open_vulns = await get_open_vulnerabilities(loaders, group_name)
    closed_vulns = await get_closed_vulnerabilities(loaders, group_name)
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
            "permanent_requested": 0,
            "permanent_approved": 0,
            "undefined": 0,
        },
        "events": {
            "unsolved": 0,
            "new": 0,
        },
        "findings": [],
        "vulns_len": 0,
    }

    findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
    findings_ids = [finding.id for finding in findings]

    group_vulns: Tuple[
        Vulnerability, ...
    ] = await loaders.finding_vulnerabilities_nzr.load_many_chained(
        findings_ids
    )

    if len(group_vulns) == 0:
        LOGGER_CONSOLE.info(f"NO vulns at {group_name}", **NOEXTRA)
        return content

    content["vulns_len"] = len(group_vulns)
    last_day = datetime_utils.get_now_minus_delta(hours=24)

    oldest_finding = await get_oldest_no_treatment(loaders, findings)
    if oldest_finding:
        max_severity, severest_finding = await get_max_open_severity(
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
        await get_mean_remediate_non_treated_severity(
            loaders, group_name, Decimal("0.0"), Decimal("10.0")
        )
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
    treatments = vulns_utils.get_total_treatment_date(group_vulns, last_day)
    content["treatments"]["temporary_applied"] = treatments.get("accepted", 0)
    content["treatments"]["permanent_requested"] = treatments.get(
        "accepted_undefined_submitted", 0
    )
    content["treatments"]["permanent_approved"] = treatments.get(
        "accepted_undefined_approved", 0
    )
    content["treatments"]["undefined"] = treatments.get(
        "undefined_treatment", 0
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
    group_stats_all: Tuple[MailContentType, ...],
) -> MailContentType:
    """Consolidate several groups stats with precalculated data"""
    # Filter out those groups with no vulns
    groups_stats: Tuple[MailContentType, ...] = tuple(
        group for group in group_stats_all if group["vulns_len"] > 0
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
        "oldest_findings": [],
        "most_severe_findings": [],
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
    findings = []
    for stat in groups_stats:
        findings_extended = [
            {
                **finding,
                "finding_group": stat["group"],
            }
            for finding in stat["findings"]
        ]
        findings.extend(findings_extended)
    total["oldest_findings"] = sorted(
        findings, key=itemgetter("oldest_age"), reverse=True
    )[:10]
    total["most_severe_findings"] = sorted(
        findings, key=itemgetter("severity"), reverse=True
    )[:10]

    return total


async def request_upgrade(
    loaders: Any,
    group_names: list[str],
    user_email: str,
) -> None:
    """
    Lead the user towards a subscription upgrade managed by our team.
    This is meant to be a temporary flow while the billing module gets ready.
    """
    enforcer = await authz.get_group_level_enforcer(user_email)
    if not all(
        enforcer(group_name, "request_group_upgrade")
        for group_name in group_names
    ):
        raise GroupNotFound()

    groups: tuple[Group, ...] = await loaders.group_typed.load_many(
        group_names
    )
    if any(group.state.has_squad for group in groups):
        raise BillingSubscriptionSameActive()

    await notifications_domain.request_groups_upgrade(user_email, groups)


async def get_creation_date(
    loaders: Any,
    group_name: str,
) -> str:
    historic: tuple[
        GroupState, ...
    ] = await loaders.group_historic_state_typed.load(group_name)
    return historic[0].modified_date
