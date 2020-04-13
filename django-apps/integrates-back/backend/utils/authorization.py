# Standard library
import contextlib
import os
from typing import Tuple

# Third party library
from casbin import Enforcer as CasbinEnforcer
from casbin_in_memory_adapter.adapter import (
    Adapter as CasbinInMemoryAdapter,
    Policies as CasbinInMemoryPolicies,
)
from django.conf import settings
from django.core.cache import cache
from rediscluster.nodemanager import RedisClusterException
from backend.dal import user as user_dal


def get_subject_cache_key(subject: str) -> str:
    return f'authorization.{subject.lower().encode().hex()}'


def get_perm_metamodel_path(name: str) -> str:
    return os.path.join(settings.BASE_DIR, 'authorization', name)


def get_subject_policies(subject: str) -> CasbinInMemoryPolicies:
    """Get all policies associated with a user."""
    subject_policies: CasbinInMemoryPolicies = tuple(
        ('p', (policy.level, policy.subject, policy.object, policy.role))
        for policy in user_dal.get_subject_policies(subject))
    return subject_policies


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
    cache.set(cache_key, fetched_data, timeout=300)

    return fetched_data


def get_manager_actions() -> Tuple[str, ...]:
    """Actions that only client's project managers can perform."""
    return (
        'backend_api_resolvers_me__get_tags',
        'backend_api_resolvers_tag_resolve_tag',
        'backend_api_resolvers_user_resolve_user_list_projects',
    )


def get_internal_manager_actions() -> Tuple[str, ...]:
    """Actions that only FluidAttacks's project managers can perform."""
    return (
        'backend_api_resolvers_project_resolve_create_project',
        'backend_api_resolvers_user_resolve_user_list_projects',
    )


def get_analyst_actions() -> Tuple[str, ...]:
    """Actions that only FluidAttacks's hackers can perform."""
    return (
        'backend_api_resolvers_cache_resolve_invalidate_cache',
    )


def get_admin_actions() -> Tuple[str, ...]:
    """Actions that only platform admins can perform."""
    return (
        'backend_api_resolvers_cache_resolve_invalidate_cache',
        'backend_api_resolvers_internal_project_resolve_project_name',
        'backend_api_resolvers_project_resolve_alive_projects',
        'backend_api_resolvers_project_resolve_create_project',
        'backend_api_resolvers_subscription__do_post_broadcast_message',
        'backend_api_resolvers_user_resolve_add_user',
    )


def list_actions() -> Tuple[str, ...]:
    all_actions = get_manager_actions() \
        + get_internal_manager_actions() \
        + get_analyst_actions() \
        + get_admin_actions()

    return tuple(set(all_actions))


def matches_permission(subject: str, role: str, action: str) -> bool:
    if action in get_manager_actions() \
            and role in ['admin', 'customeradmin']:
        matches = True
    elif action in get_internal_manager_actions():
        matches = \
            role == 'admin' \
            or role in ['customer', 'customeradmin'] \
            and subject.endswith('@fluidattacks.com')
    elif action in get_analyst_actions():
        matches = role in ['admin', 'analyst']
    elif action in get_admin_actions():
        matches = role == 'admin'
    else:
        matches = False

    return matches


def get_user_level_enforcer(subject: str) -> CasbinEnforcer:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)
    adapter = CasbinInMemoryAdapter(policies)

    return CasbinEnforcer(
        model=get_perm_metamodel_path('user_level.conf'),
        adapter=adapter,
    )


def get_user_level_enforcer_async(subject: str) -> CasbinEnforcer:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)
    adapter = CasbinInMemoryAdapter(policies)

    enforcer = CasbinEnforcer(
        model=get_perm_metamodel_path('user_level_async.conf'),
        adapter=adapter,
    )

    enforcer.fm.add_function('matchesPermission', matches_permission)

    return enforcer


def get_group_level_enforcer(subject: str) -> CasbinEnforcer:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)
    adapter = CasbinInMemoryAdapter(policies)

    return CasbinEnforcer(
        model=get_perm_metamodel_path('group_level.conf'),
        adapter=adapter,
    )


def get_group_level_enforcer_async(subject: str) -> CasbinEnforcer:
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
