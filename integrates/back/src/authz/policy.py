from aioextensions import (
    collect,
)
from authz.model import (
    get_group_level_roles_model,
    get_organization_level_roles_model,
    get_user_level_roles_model,
)
from boto3.dynamodb.conditions import (
    Key,
)
from botocore.exceptions import (
    ClientError,
)
import contextlib
from contextlib import (
    suppress,
)
from custom_exceptions import (
    StakeholderNotFound,
    StakeholderNotInGroup,
    StakeholderNotInOrganization,
)
from custom_types import (
    DynamoDelete as DynamoDeleteType,
)
from db_model import (
    group_access as group_access_model,
    organization_access as organization_access_model,
    stakeholders as stakeholders_model,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
)
from db_model.groups.enums import (
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
)
from db_model.groups.types import (
    Group,
)
from db_model.organization_access.types import (
    OrganizationAccess,
    OrganizationAccessMetadataToUpdate,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderMetadataToUpdate,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from functools import (
    partial,
)
import logging
import logging.config
from newutils import (
    function,
)
from redis_cluster.operations import (
    redis_del_by_deps,
    redis_get_or_set_entity_attr,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Awaitable,
    cast,
    DefaultDict,
    NamedTuple,
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
AUTHZ_TABLE: str = "fi_authz"
LOGGER = logging.getLogger(__name__)


class ServicePolicy(NamedTuple):
    group_name: str
    service: str


class SubjectPolicy(NamedTuple):
    level: str
    subject: str
    object: str
    role: str


def _cast_dict_into_subject_policy(item: dict[str, str]) -> SubjectPolicy:
    field_types: dict[Any, Any] = SubjectPolicy.__annotations__

    # Every string as lowercase
    for field, _ in field_types.items():
        if isinstance(item.get(field), str):
            item[field] = item[field].lower()
    return SubjectPolicy(
        **{
            field: (
                item[field]
                if field in item and isinstance(item[field], typing)
                else typing()
            )
            for field, typing in field_types.items()
        }
    )


def _cast_subject_policy_into_dict(policy: SubjectPolicy) -> dict[str, str]:
    """Cast a subject policy into a dict, valid to be put in dynamo."""
    return {
        key: (value.lower() if isinstance(value, str) else value)
        for key, value in policy._asdict().items()
    }


async def _delete_subject_policy(subject: str, object_: str) -> bool:
    with contextlib.suppress(ClientError):
        delete_attrs = DynamoDeleteType(
            Key={
                "subject": subject.lower(),
                "object": object_.lower(),
            }
        )
        response = await dynamodb_ops.delete_item(AUTHZ_TABLE, delete_attrs)
        return response
    LOGGER.error(
        "Error in stakeholders_dal.delete_subject_policy",
        extra={"extra": locals()},
    )
    return False


async def _get_group_service_policies(group: Group) -> tuple[str, ...]:
    """Cached function to get 1 group features authorization policies."""
    policies: tuple[str, ...] = tuple(
        policy.service
        for policy in await _get_service_policies(group)
        if policy.group_name == group.name
    )
    return policies


async def _get_service_policies(group: Group) -> list[ServicePolicy]:
    """Return a list of policies for the given group."""
    has_squad = group.state.has_squad
    has_asm = group.state.status == GroupStateStatus.ACTIVE
    service = group.state.service
    type_ = group.state.type
    has_machine_squad: bool = has_squad or group.state.has_machine

    business_rules = (
        (has_asm, "asm"),
        (
            type_ == GroupSubscriptionType.CONTINUOUS
            and has_asm
            and has_machine_squad,
            "report_vulnerabilities",
        ),
        (service == GroupService.BLACK and has_asm, "service_black"),
        (service == GroupService.WHITE and has_asm, "service_white"),
        (
            type_ == GroupSubscriptionType.CONTINUOUS and has_asm,
            "forces",
        ),
        (
            type_ == GroupSubscriptionType.CONTINUOUS
            and has_asm
            and has_squad,
            "squad",
        ),
        (type_ == GroupSubscriptionType.CONTINUOUS, "continuous"),
        (
            type_ == GroupSubscriptionType.ONESHOT and has_asm,
            "report_vulnerabilities",
        ),
        (
            type_ == GroupSubscriptionType.ONESHOT and has_asm and has_squad,
            "squad",
        ),
    )

    return [
        ServicePolicy(group_name=group.name, service=policy_name)
        for condition, policy_name in business_rules
        if condition
    ]


async def _get_subject_policies(subject: str) -> list[SubjectPolicy]:
    """Return a list of policies for the given subject."""
    query_params = {
        "ConsistentRead": True,
        "KeyConditionExpression": Key("subject").eq(subject.lower()),
    }
    response = await dynamodb_ops.query(AUTHZ_TABLE, query_params)
    return list(map(_cast_dict_into_subject_policy, response))


async def _get_subject_policy(subject: str, object_: str) -> SubjectPolicy:
    """Return a policy for the given subject over the given object."""
    response = {}
    query_attrs = {
        "ConsistentRead": True,
        "KeyConditionExpression": (
            Key("subject").eq(subject.lower())
            & Key("object").eq(object_.lower())
        ),
    }
    response_items = await dynamodb_ops.query(AUTHZ_TABLE, query_attrs)
    if response_items:
        response = response_items[0]
    return _cast_dict_into_subject_policy(response)


async def get_user_subject_policies(
    subject: str,
) -> tuple[tuple[str, str, str], ...]:
    policies: tuple[tuple[str, str, str], ...] = tuple(
        (policy.level, policy.object, policy.role)
        for policy in await _get_subject_policies(subject)
        if policy.subject == subject
    )
    return policies


async def get_cached_group_service_policies(
    group: Group,
) -> tuple[str, ...]:
    response: tuple[str, ...] = await redis_get_or_set_entity_attr(
        partial(_get_group_service_policies, group),
        entity="authz_group",
        attr="policies",
        name=group.name,
        ttl=86400,
    )
    return response


async def get_cached_subject_policies(
    subject: str,
    context_store: Optional[DefaultDict[Any, Any]] = None,
    with_cache: bool = True,
) -> tuple[tuple[str, str, str], ...]:
    """Cached function to get 1 user authorization policies."""
    policies: tuple[tuple[str, str, str], ...]

    if with_cache:
        # Unique ID for this function and arguments
        context_store_key: str = function.get_id(
            get_cached_subject_policies,
            subject,
        )

        # If there is already a result for this operation within the context of
        # this request let's return it
        context_store = context_store or DefaultDict(str)
        if context_store_key in context_store:
            return cast(
                tuple[tuple[str, str, str], ...],
                context_store[context_store_key],
            )

        policies = await redis_get_or_set_entity_attr(
            partial(get_user_subject_policies, subject),
            entity="authz_subject",
            attr="policies",
            id=subject.lower(),
            ttl=86400,
        )
        context_store[context_store_key] = policies
        return policies
    # Let's fetch the data from the database
    policies = await get_user_subject_policies(subject)
    return policies


async def get_group_level_role(
    loaders: Any,
    email: str,
    group_name: str,
) -> str:
    group_role: str = ""
    # Admins are granted access to all groups
    if loaders:
        with suppress(StakeholderNotInGroup):
            group_access: GroupAccess = await loaders.group_access.load(
                (group_name, email)
            )
            if group_access.role:
                group_role = group_access.role

    if not group_role:
        subject_policy = await _get_subject_policy(email, group_name)
        group_role = subject_policy.role

    # Please always make the query at the end
    if not group_role and await get_user_level_role(loaders, email) == "admin":
        return "admin"

    return group_role


async def get_group_level_roles(
    loaders: Any,
    email: str,
    groups: list[str],
    with_cache: bool = True,
) -> dict[str, str]:
    is_admin: bool = await get_user_level_role(loaders, email) == "admin"

    if loaders:
        groups_access: tuple[
            GroupAccess, ...
        ] = await loaders.stakeholder_groups_access.load(email)
        db_roles: dict[str, str] = {
            access.group_name: access.role
            for access in groups_access
            if access.role
        }
    else:
        policies = await get_cached_subject_policies(
            email, with_cache=with_cache
        )
        db_roles = {
            object_: role
            for level, object_, role in policies
            if level == "group"
        }

    return {
        group: "admin"
        if is_admin and group not in db_roles
        else db_roles.get(group, "")
        for group in groups
    }


async def get_organization_level_role(
    loaders: Any,
    email: str,
    organization_id: str,
) -> str:
    organization_role: str = ""
    # Admins are granted access to all organizations
    if loaders:
        with suppress(StakeholderNotInOrganization):
            org_access: OrganizationAccess = (
                await loaders.organization_access.load(
                    (organization_id, email)
                )
            )
            if org_access.role:
                organization_role = org_access.role

    if not organization_role:
        subject_policy = await _get_subject_policy(
            email, organization_id.lower()
        )
        organization_role = subject_policy.role

    # Please always make the query at the end
    if (
        not organization_role
        and await get_user_level_role(loaders, email) == "admin"
    ):
        return "admin"

    return organization_role


async def get_user_level_role(
    loaders: Any,
    email: str,
) -> str:
    user_role: str = ""
    if loaders:
        with suppress(StakeholderNotFound):
            stakeholder: Stakeholder = await loaders.stakeholder.load(email)
            if stakeholder.role:
                user_role = stakeholder.role

    if not user_role:
        user_policy = await _get_subject_policy(email, "self")
        user_role = str(user_policy.role)

    return user_role


async def grant_group_level_role(
    loaders: Any,
    email: str,
    group_name: str,
    role: str,
) -> bool:
    if role not in get_group_level_roles_model(email):
        raise ValueError(f"Invalid role value: {role}")

    await group_access_model.update_metadata(
        email=email,
        group_name=group_name,
        metadata=GroupAccessMetadataToUpdate(role=role),
    )
    policy = SubjectPolicy(
        level="group",
        subject=email,
        object=group_name,
        role=role,
    )
    success: bool = False
    coroutines: list[Awaitable[bool]] = []
    coroutines.append(put_subject_policy(policy))

    # If there is no user-level role for this user add one
    if not await get_user_level_role(loaders, email):
        user_level_role: str = (
            role if role in get_user_level_roles_model(email) else "user"
        )
        coroutines.append(grant_user_level_role(email, user_level_role))
    success = await collect(coroutines)
    return success and await revoke_cached_subject_policies(email)


async def grant_organization_level_role(
    loaders: Any,
    email: str,
    organization_id: str,
    role: str,
) -> bool:
    if role not in get_organization_level_roles_model(email):
        raise ValueError(f"Invalid role value: {role}")

    await organization_access_model.update_metadata(
        email=email,
        organization_id=organization_id,
        metadata=OrganizationAccessMetadataToUpdate(role=role),
    )
    policy = SubjectPolicy(
        level="organization",
        subject=email,
        object=organization_id,
        role=role,
    )
    success: bool = False
    coroutines: list[Awaitable[bool]] = []
    coroutines.append(put_subject_policy(policy))

    # If there is no user-level role for this user add one
    if not await get_user_level_role(loaders, email):
        user_level_role: str = (
            role if role in get_user_level_roles_model(email) else "user"
        )
        coroutines.append(grant_user_level_role(email, user_level_role))
    success = await collect(coroutines)
    return success and await revoke_cached_subject_policies(email)


async def grant_user_level_role(email: str, role: str) -> bool:
    if role not in get_user_level_roles_model(email):
        raise ValueError(f"Invalid role value: {role}")

    await stakeholders_model.update_metadata(
        email=email,
        metadata=StakeholderMetadataToUpdate(role=role),
    )
    policy = SubjectPolicy(
        level="user",
        subject=email,
        object="self",
        role=role,
    )
    return await put_subject_policy(
        policy
    ) and await revoke_cached_subject_policies(email)


async def has_access_to_group(
    loaders: Any,
    email: str,
    group_name: str,
) -> bool:
    """Verify if the user has access to a group."""
    return bool(await get_group_level_role(loaders, email, group_name.lower()))


async def put_subject_policy(policy: SubjectPolicy) -> bool:
    item = _cast_subject_policy_into_dict(policy)
    with contextlib.suppress(ClientError):
        response = await dynamodb_ops.put_item(AUTHZ_TABLE, item)
        return response
    LOGGER.error(
        "Error in stakeholders_dal.put_subject_policy",
        extra={"extra": locals()},
    )
    return False


async def revoke_cached_group_service_policies(group_name: str) -> bool:
    """Revoke the cached policies for the provided group."""
    # Delete the cache key from the cache
    await redis_del_by_deps(
        "revoke_authz_group",
        authz_group_name=group_name.lower(),
    )
    return True


async def revoke_cached_subject_policies(subject: str) -> bool:
    """Revoke the cached policies for the provided subject."""
    await redis_del_by_deps(
        "revoke_authz_subject",
        authz_subject_id=subject.lower(),
    )
    return True


async def revoke_group_level_role(email: str, group_name: str) -> bool:
    return await _delete_subject_policy(
        email, group_name
    ) and await revoke_cached_subject_policies(email)


async def revoke_organization_level_role(
    email: str, organization_id: str
) -> bool:
    return await _delete_subject_policy(
        email, organization_id
    ) and await revoke_cached_subject_policies(email)


async def revoke_user_level_role(email: str) -> bool:
    return await _delete_subject_policy(
        email, "self"
    ) and await revoke_cached_subject_policies(email)
