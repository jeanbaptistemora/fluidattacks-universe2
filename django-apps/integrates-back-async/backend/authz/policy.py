# Standard library
import contextlib
from typing import (
    Tuple,
)

# Third party library
from django.core.cache import cache
from rediscluster.nodemanager import RedisClusterException

# Local imports
from backend.dal import (
    project as project_dal,
    user as user_dal,
)
from .model import (
    USER_LEVEL_ROLES,
    GROUP_LEVEL_ROLES,
)


def get_group_cache_key(group: str) -> str:
    return f'authorization.group.{group.lower().encode().hex()}'


def get_subject_cache_key(subject: str) -> str:
    return f'authorization.subject.{subject.lower().encode().hex()}'


def get_cached_group_service_attributes_policies(
    group: str,
) -> Tuple[Tuple[str, str], ...]:
    """Cached function to get 1 group features authorization policies."""
    cache_key: str = get_group_cache_key(group)

    # Attempt to retrieve data from the cache
    with contextlib.suppress(RedisClusterException):
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

    # Let's fetch the data from the database
    fetched_data = tuple(
        (policy.group, policy.service)
        for policy in project_dal.get_service_policies(group))

    # Put the data in the cache
    cache.set(cache_key, fetched_data, timeout=60 * 60)

    return fetched_data


def get_cached_subject_policies(
    subject: str,
) -> Tuple[Tuple[str, str, str, str], ...]:
    """Cached function to get 1 user authorization policies."""
    cache_key: str = get_subject_cache_key(subject)

    # Attempt to retrieve data from the cache
    with contextlib.suppress(RedisClusterException):
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

    # Let's fetch the data from the database
    fetched_data = tuple(
        (policy.level, policy.subject, policy.object, policy.role)
        for policy in user_dal.get_subject_policies(subject))

    # Put the data in the cache
    cache.set(cache_key, fetched_data, timeout=300)

    return fetched_data


def get_group_level_role(email: str, group: str) -> str:
    # Admins are granted access to all groups
    if get_user_level_role(email) == 'admin':
        return 'admin'

    return user_dal.get_subject_policy(email, group).role


def get_user_level_role(email: str) -> str:
    return user_dal.get_subject_policy(email, 'self').role


def grant_group_level_role(email: str, group: str, role: str) -> bool:
    if role not in GROUP_LEVEL_ROLES:
        raise ValueError(f'Invalid role value: {role}')

    policy = user_dal.SUBJECT_POLICY(
        level='group',
        subject=email,
        object=group,
        role=role,
    )

    success: bool = True

    # If there is no user-level role for this user add one
    if not get_user_level_role(email):
        user_level_role: str = \
            role if role in USER_LEVEL_ROLES else 'customer'
        success = success and grant_user_level_role(email, user_level_role)

    return success \
        and user_dal.put_subject_policy(policy) \
        and revoke_cached_subject_policies(email)


def grant_user_level_role(email: str, role: str) -> bool:
    if role not in USER_LEVEL_ROLES:
        raise ValueError(f'Invalid role value: {role}')

    policy = user_dal.SUBJECT_POLICY(
        level='user',
        subject=email,
        object='self',
        role=role,
    )

    return user_dal.put_subject_policy(policy) \
        and revoke_cached_subject_policies(email)


def revoke_cached_subject_policies(subject: str) -> bool:
    """Revoke the cached policies for the provided subject."""
    cache_key: str = get_subject_cache_key(subject)

    # Delete the cache key from the cache
    cache.delete_pattern(f'*{cache_key}*')

    # Refresh the cache key as the user is probably going to use it soon :)
    get_cached_subject_policies(subject)

    return True


def revoke_group_level_role(email: str, group: str) -> bool:
    return user_dal.delete_subject_policy(email, group) \
        and revoke_cached_subject_policies(email)


def revoke_user_level_role(email: str) -> bool:
    return user_dal.delete_subject_policy(email, 'self') \
        and revoke_cached_subject_policies(email)
