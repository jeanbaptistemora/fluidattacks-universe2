from .model import (
    get_group_level_roles_model,
    get_organization_level_roles_model,
    get_user_level_roles_model,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from botocore.exceptions import (
    ClientError,
)
import contextlib
from custom_types import (
    DynamoDelete as DynamoDeleteType,
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
from newutils.utils import (
    get_key_or_fallback,
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
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

logging.config.dictConfig(LOGGING)

# Constants
AUTHZ_TABLE: str = "fi_authz"
GROUPS_TABLE: str = "FI_projects"
LOGGER = logging.getLogger(__name__)

# Typing
ServicePolicy = NamedTuple("ServicePolicy", [("group", str), ("service", str)])
SubjectPolicy = NamedTuple(
    "SubjectPolicy",
    [
        ("level", str),
        ("subject", str),
        ("object", str),
        ("role", str),
    ],
)


def _cast_dict_into_subject_policy(item: Dict[str, str]) -> SubjectPolicy:
    field_types: Dict[Any, Any] = SubjectPolicy.__annotations__

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


def _cast_subject_policy_into_dict(policy: SubjectPolicy) -> Dict[str, str]:
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
        "Error in users_dal.delete_subject_policy", extra={"extra": locals()}
    )
    return False


async def _get_group_service_policies(group: str) -> Tuple[str, ...]:
    """Cached function to get 1 group features authorization policies."""
    policies: Tuple[str, ...] = tuple(
        policy.service
        for policy in await _get_service_policies(group)
        if policy.group == group
    )
    return policies


async def _get_service_policies(group: str) -> List[ServicePolicy]:
    """Return a list of policies for the given group."""
    query_attrs = {
        "KeyConditionExpression": Key("project_name").eq(group.lower()),
        "ConsistentRead": True,
        "ProjectionExpression": "historic_configuration, project_status",
    }
    response_items = await dynamodb_ops.query(GROUPS_TABLE, query_attrs)

    # There is no such group, let's make an early return
    if not response_items:
        return []

    group_attributes = response_items[0]
    historic_config = group_attributes["historic_configuration"]
    has_squad: bool = get_key_or_fallback(
        historic_config[-1], "has_squad", "has_drills"
    )
    has_forces: bool = historic_config[-1]["has_forces"]
    has_asm: bool = (
        get_key_or_fallback(group_attributes, "group_status", "project_status")
        == "ACTIVE"
    )
    service = historic_config[-1]["service"]
    type_: str = historic_config[-1]["type"]

    business_rules = (
        (has_asm, "asm"),
        (service == "BLACK" and has_asm, "service_black"),
        (service == "WHITE" and has_asm, "service_white"),
        (
            type_ == "continuous" and has_asm and has_forces,
            "forces",
        ),
        (type_ == "continuous" and has_asm and has_squad, "squad"),
        (type_ == "continuous", "continuous"),
        (type_ == "oneshot" and has_asm and has_squad, "squad"),
    )

    return [
        ServicePolicy(group=group, service=policy_name)
        for condition, policy_name in business_rules
        if condition
    ]


async def _get_subject_policies(subject: str) -> List[SubjectPolicy]:
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


async def _get_user_subject_policies(
    subject: str,
) -> Tuple[Tuple[str, str, str], ...]:
    policies: Tuple[Tuple[str, str, str], ...] = tuple(
        (policy.level, policy.object, policy.role)
        for policy in await _get_subject_policies(subject)
        if policy.subject == subject
    )
    return policies


async def get_cached_group_service_policies(group: str) -> Tuple[str, ...]:
    response: Tuple[str, ...] = await redis_get_or_set_entity_attr(
        partial(_get_group_service_policies, group),
        entity="authz_group",
        attr="policies",
        name=group.lower(),
        ttl=86400,
    )
    return response


async def get_cached_subject_policies(
    subject: str,
    context_store: Optional[DefaultDict[Any, Any]] = None,
    with_cache: bool = True,
) -> Tuple[Tuple[str, str, str], ...]:
    """Cached function to get 1 user authorization policies."""
    policies: Tuple[Tuple[str, str, str], ...]

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
                Tuple[Tuple[str, str, str], ...],
                context_store[context_store_key],
            )

        policies = await redis_get_or_set_entity_attr(
            partial(_get_user_subject_policies, subject),
            entity="authz_subject",
            attr="policies",
            id=subject.lower(),
            ttl=86400,
        )
        context_store[context_store_key] = policies
        return policies
    # Let's fetch the data from the database
    policies = await _get_user_subject_policies(subject)
    return policies


async def get_group_level_role(email: str, group: str) -> str:
    # Admins are granted access to all groups
    subject_policy = await _get_subject_policy(email, group)
    group_role: str = subject_policy.role

    # Please always make the query at the end
    if not group_role and await get_user_level_role(email) == "admin":
        return "admin"
    return group_role


async def get_group_level_roles(
    email: str, groups: List[str]
) -> Dict[str, str]:
    is_admin: bool = await get_user_level_role(email) == "admin"
    policies = await get_cached_subject_policies(email)
    db_roles: Dict[str, str] = {
        object_: role for level, object_, role in policies if level == "group"
    }
    return {
        group: "admin"
        if is_admin and group not in db_roles
        else db_roles.get(group, "")
        for group in groups
    }


async def get_organization_level_role(email: str, organization_id: str) -> str:
    # Admins are granted access to all organizations
    subject_policy = await _get_subject_policy(email, organization_id.lower())
    organization_role: str = subject_policy.role

    # Please always make the query at the end
    if not organization_role and await get_user_level_role(email) == "admin":
        return "admin"
    return organization_role


async def get_user_level_role(email: str) -> str:
    user_policy = await _get_subject_policy(email, "self")
    return str(user_policy.role)


async def grant_group_level_role(email: str, group: str, role: str) -> bool:
    if role not in get_group_level_roles_model(email):
        raise ValueError(f"Invalid role value: {role}")

    policy = SubjectPolicy(
        level="group",
        subject=email,
        object=group,
        role=role,
    )
    success: bool = False
    coroutines: List[Awaitable[bool]] = []
    coroutines.append(put_subject_policy(policy))

    # If there is no user-level role for this user add one
    if not await get_user_level_role(email):
        user_level_role: str = (
            role if role in get_user_level_roles_model(email) else "customer"
        )
        coroutines.append(grant_user_level_role(email, user_level_role))
    success = await collect(coroutines)
    return success and await revoke_cached_subject_policies(email)


async def grant_organization_level_role(
    email: str, organization: str, role: str
) -> bool:
    if role not in get_organization_level_roles_model(email):
        raise ValueError(f"Invalid role value: {role}")

    policy = SubjectPolicy(
        level="organization",
        subject=email,
        object=organization,
        role=role,
    )
    success: bool = False
    coroutines: List[Awaitable[bool]] = []
    coroutines.append(put_subject_policy(policy))

    # If there is no user-level role for this user add one
    if not await get_user_level_role(email):
        user_level_role: str = (
            role if role in get_user_level_roles_model(email) else "customer"
        )
        coroutines.append(grant_user_level_role(email, user_level_role))
    success = await collect(coroutines)
    return success and await revoke_cached_subject_policies(email)


async def grant_user_level_role(email: str, role: str) -> bool:
    if role not in get_user_level_roles_model(email):
        raise ValueError(f"Invalid role value: {role}")

    policy = SubjectPolicy(
        level="user",
        subject=email,
        object="self",
        role=role,
    )
    return await put_subject_policy(
        policy
    ) and await revoke_cached_subject_policies(email)


async def has_access_to_group(email: str, group: str) -> bool:
    """Verify if the user has access to a group."""
    return bool(await get_group_level_role(email, group.lower()))


async def put_subject_policy(policy: SubjectPolicy) -> bool:
    item = _cast_subject_policy_into_dict(policy)
    with contextlib.suppress(ClientError):
        response = await dynamodb_ops.put_item(AUTHZ_TABLE, item)
        return response
    LOGGER.error(
        "Error in users_dal.put_subject_policy", extra={"extra": locals()}
    )
    return False


async def revoke_cached_group_service_policies(group: str) -> bool:
    """Revoke the cached policies for the provided group."""
    # Delete the cache key from the cache
    await redis_del_by_deps(
        "revoke_authz_group",
        authz_group_name=group.lower(),
    )
    return True


async def revoke_cached_subject_policies(subject: str) -> bool:
    """Revoke the cached policies for the provided subject."""
    await redis_del_by_deps(
        "revoke_authz_subject",
        authz_subject_id=subject.lower(),
    )
    return True


async def revoke_group_level_role(email: str, group: str) -> bool:
    return await _delete_subject_policy(
        email, group
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
