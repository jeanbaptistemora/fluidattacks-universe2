# Standard library
from functools import (
    partial,
)
from typing import (
    Any,
    Awaitable,
    DefaultDict,
    Dict,
    List,
    Optional,
    Tuple,
    cast
)
import logging

# Third party library
from aioextensions import (
    collect,
)

# Local imports
from backend.dal import (
    project as project_dal,
    user as user_dal,
)
from backend.dal.helpers.redis import (
    REDIS_EXCEPTIONS,
    redis_del_by_deps,
    redis_get_or_set_entity_attr,
)
from backend.utils import (
    function,
)
from backend.utils.encodings import (
    safe_encode,
)
from backend import util

from back.settings import LOGGING
from .model import (
    USER_LEVEL_ROLES,
    GROUP_LEVEL_ROLES,
    ORGANIZATION_LEVEL_ROLES
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def get_subject_cache_key(subject: str) -> str:
    return f'authorization.subject.{safe_encode(subject.lower())}'


async def _get_group_service_attributes_policies(
    group: str,
) -> Tuple[str, ...]:
    """Cached function to get 1 group features authorization policies."""
    policies: Tuple[str, ...] = tuple(
        policy.service
        for policy in await project_dal.get_service_policies(group)
        if policy.group == group
    )

    return policies


async def get_cached_group_service_attributes_policies(
    group: str,
) -> Tuple[str, ...]:
    response: Tuple[str, ...] = await redis_get_or_set_entity_attr(
        partial(_get_group_service_attributes_policies, group),
        entity='authz_group',
        attr='policies',
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
    if with_cache:
        # Unique ID for this function and arguments
        context_store_key: str = function.get_id(
            get_cached_subject_policies, subject,
        )

        # If there is already a result for this operation within the context of
        # this request let's return it
        context_store = context_store or DefaultDict(str)
        if context_store_key in context_store:
            return cast(
                Tuple[Tuple[str, str, str], ...],
                context_store[context_store_key]
            )

        cache_key: str = get_subject_cache_key(subject)

        try:
            # Attempt to retrieve data from the cache
            ret = await util.get_redis_element(cache_key)
        except REDIS_EXCEPTIONS:
            ret = None

        if ret is None:
            # Let's fetch the data from the database
            policies = tuple(
                (policy.level, policy.object, policy.role)
                for policy in await user_dal.get_subject_policies(subject)
                if policy.subject == subject
            )

            try:
                # Put the data in the cache
                await util.set_redis_element(
                    cache_key,
                    policies,
                    ttl=300
                )
            except REDIS_EXCEPTIONS as ex:
                LOGGER.exception(ex, extra={'extra': locals()})
        else:
            policies = cast(Tuple[Tuple[str, str, str], ...], ret)
        context_store[context_store_key] = policies
        return policies
    # Let's fetch the data from the database
    policies = tuple(
        (policy.level, policy.object, policy.role)
        for policy in await user_dal.get_subject_policies(subject)
        if policy.subject == subject
    )

    return policies


async def get_group_level_role(email: str, group: str) -> str:
    # Admins are granted access to all groups
    subject_policy = await user_dal.get_subject_policy(email, group)
    group_role: str = subject_policy.role

    # Please always make the query at the end
    if not group_role and await get_user_level_role(email) == 'admin':
        return 'admin'

    return group_role


async def get_organization_level_role(email: str, organization_id: str) -> str:
    # Admins are granted access to all organizations
    subject_policy = await user_dal.get_subject_policy(
        email, organization_id.lower()
    )
    organization_role: str = subject_policy.role

    # Please always make the query at the end
    if not organization_role and await get_user_level_role(email) == 'admin':
        return 'admin'

    return organization_role


async def get_group_level_roles(
        email: str, groups: List[str]) -> Dict[str, str]:
    is_admin: bool = await get_user_level_role(email) == 'admin'
    policies = await get_cached_subject_policies(email)

    db_roles: Dict[str, str] = {
        object_: role
        for level, object_, role in policies
        if level == 'group'
    }

    return {
        group: 'admin'
        if is_admin and group not in db_roles
        else db_roles.get(group, '')
        for group in groups
    }


async def get_user_level_role(email: str) -> str:
    user_policy = await user_dal.get_subject_policy(email, 'self')
    return user_policy.role


async def grant_group_level_role(email: str, group: str, role: str) -> bool:
    if role not in GROUP_LEVEL_ROLES:
        raise ValueError(f'Invalid role value: {role}')

    policy = user_dal.SubjectPolicy(
        level='group',
        subject=email,
        object=group,
        role=role,
    )

    success: bool = False
    coroutines: List[Awaitable[bool]] = []
    coroutines.append(user_dal.put_subject_policy(policy))

    # If there is no user-level role for this user add one
    if not await get_user_level_role(email):
        user_level_role: str = \
            role if role in USER_LEVEL_ROLES else 'customer'
        coroutines.append(grant_user_level_role(email, user_level_role))

    success = await collect(coroutines)

    return success and await revoke_cached_subject_policies(email)


async def grant_organization_level_role(
    email: str,
    organization: str,
    role: str
) -> bool:
    if role not in ORGANIZATION_LEVEL_ROLES:
        raise ValueError(f'Invalid role value: {role}')

    policy = user_dal.SubjectPolicy(
        level='organization',
        subject=email,
        object=organization,
        role=role,
    )

    success: bool = False
    coroutines: List[Awaitable[bool]] = []
    coroutines.append(user_dal.put_subject_policy(policy))

    # If there is no user-level role for this user add one
    if not await get_user_level_role(email):
        user_level_role: str = (
            role
            if role in USER_LEVEL_ROLES
            else 'customer'
        )
        coroutines.append(grant_user_level_role(email, user_level_role))

    success = await collect(coroutines)

    return success and await revoke_cached_subject_policies(email)


async def grant_user_level_role(email: str, role: str) -> bool:
    if role not in USER_LEVEL_ROLES:
        raise ValueError(f'Invalid role value: {role}')

    policy = user_dal.SubjectPolicy(
        level='user',
        subject=email,
        object='self',
        role=role,
    )

    return (await user_dal.put_subject_policy(policy) and
            await revoke_cached_subject_policies(email))


async def revoke_cached_group_service_attributes_policies(group: str) -> bool:
    """Revoke the cached policies for the provided group."""
    # Delete the cache key from the cache
    return await redis_del_by_deps(
        'revoke_authz_group',
        authz_group_name=group.lower(),
    )


async def revoke_cached_subject_policies(subject: str) -> bool:
    """Revoke the cached policies for the provided subject."""
    cache_key: str = get_subject_cache_key(subject)

    # Delete the cache key from the cache
    await util.del_redis_element(f'*{cache_key}*')

    # Refresh the cache key as the user is probably going to use it soon :)
    await get_cached_subject_policies(subject)

    return True


async def revoke_group_level_role(email: str, group: str) -> bool:
    return (await user_dal.delete_subject_policy(email, group) and
            await revoke_cached_subject_policies(email))


async def revoke_organization_level_role(
        email: str, organization_id: str) -> bool:
    return (await user_dal.delete_subject_policy(email, organization_id) and
            await revoke_cached_subject_policies(email))


async def revoke_user_level_role(email: str) -> bool:
    return (await user_dal.delete_subject_policy(email, 'self') and
            await revoke_cached_subject_policies(email))
