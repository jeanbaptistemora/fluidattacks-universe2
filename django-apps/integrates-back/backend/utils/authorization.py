# Standard library
import contextlib
import os
from typing import (
    Tuple,
)

# Third party library
from casbin import Enforcer as CasbinEnforcer
from casbin_in_memory_adapter.adapter import (
    Adapter as CasbinInMemoryAdapter,
    Policy as CasbinInMemoryPolicy,
    Rule as CasbinInMemoryRule,
)
from django.conf import settings
from django.core.cache import cache
from rediscluster.nodemanager import RedisClusterException


def get_subject_cache_key(subject: str) -> str:
    return f'authorization.{subject.lower().encode().hex()}'


def get_perm_metamodel_path(name: str) -> str:
    return os.path.join(settings.BASE_DIR, 'authorization', name)


def get_subject_policies(subject: str):
    """Get all policies associated with a user."""
    user_level_policies: Tuple[CasbinInMemoryRule, ...] = \
        tuple(settings.CASBIN_ADAPTER.get_rules('p', 'p', ['user', subject]))
    group_level_policies: Tuple[CasbinInMemoryRule, ...] = \
        tuple(settings.CASBIN_ADAPTER.get_rules('p', 'p', ['group', subject]))

    all_policies: CasbinInMemoryPolicy = []
    all_policies.extend(
        ('p', user_level_policy)
        for user_level_policy in user_level_policies)
    all_policies.extend(
        ('p', group_level_policy)
        for group_level_policy in group_level_policies)

    return all_policies


def get_cached_subject_policies(subject: str):
    """Cached function to get 1 user authorization policies."""
    cache_key: str = get_subject_cache_key(subject)

    # Attempt to retrieve data from the cache
    with contextlib.suppress(RedisClusterException):
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

    # Let's fetch the data from the database
    fetched_data = get_subject_policies(subject)

    # Put the data in the cache
    cache.set(cache_key, fetched_data, timeout=3600)

    return fetched_data


def get_user_level_authorization_enforcer(subject: str) -> CasbinEnforcer:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)
    adapter = CasbinInMemoryAdapter(policies)

    return CasbinEnforcer(
        model=get_perm_metamodel_path('user_level.conf'),
        adapter=adapter,
    )


def get_user_level_authorization_enforcer_async(subject: str) -> CasbinEnforcer:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)
    adapter = CasbinInMemoryAdapter(policies)

    return CasbinEnforcer(
        model=get_perm_metamodel_path('user_level_async.conf'),
        adapter=adapter,
    )


def get_group_level_authorization_enforcer(subject: str) -> CasbinEnforcer:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)
    adapter = CasbinInMemoryAdapter(policies)

    return CasbinEnforcer(
        model=get_perm_metamodel_path('group_level.conf'),
        adapter=adapter,
    )


def get_group_level_authorization_enforcer_async(subject: str) -> CasbinEnforcer:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)
    adapter = CasbinInMemoryAdapter(policies)

    return CasbinEnforcer(
        model=get_perm_metamodel_path('group_level_async.conf'),
        adapter=adapter,
    )


def revoke_cached_subject_policies(subject: str) -> bool:
    """Revoke the cached policies for the provided subject."""
    cache_key: str = get_subject_cache_key(subject)

    # Delete the cache key from the cache
    cache.delete_pattern(f'*{cache_key}*')

    # Refresh the cache key as the user is probably going to use it soon :)
    get_cached_subject_policies(subject)

    return True
