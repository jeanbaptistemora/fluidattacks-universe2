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


def get_basic_actions() -> Tuple[str, ...]:
    """Actions that everyone can perform."""
    return (
        'backend_api_resolvers_alert_resolve_alert',
        'backend_api_resolvers_event__do_add_event_comment',
        'backend_api_resolvers_event__do_download_event_file',
        'backend_api_resolvers_event_resolve_event',
        'backend_api_resolvers_event_resolve_events',
        'backend_api_resolvers_finding__do_add_finding_comment',
        'backend_api_resolvers_finding_resolve_finding',
        'backend_api_resolvers_forces_resolve_forces_executions',
        'backend_api_resolvers_project__get_comments',
        'backend_api_resolvers_project__get_events',
        'backend_api_resolvers_project_resolve_add_project_comment',
        'backend_api_resolvers_project_resolve_project',
        'backend_api_resolvers_resource__do_download_file',
        'backend_api_resolvers_resource_resolve_resources',
    )


def get_customer_actions() -> Tuple[str, ...]:
    """Actions that only client's users can perform."""
    return (
        'backend_api_resolvers_finding__do_update_client_description',
        'backend_api_resolvers_project_resolve_add_tags',
        'backend_api_resolvers_project_resolve_remove_tag',
        'backend_api_resolvers_resource__do_add_environments',
        'backend_api_resolvers_resource__do_add_files',
        'backend_api_resolvers_resource__do_add_repositories',
        'backend_api_resolvers_resource__do_remove_files',
        'backend_api_resolvers_resource__do_update_environment',
        'backend_api_resolvers_resource__do_update_repository',
        'backend_api_resolvers_resource_resolve_add_resources',
        'backend_api_resolvers_vulnerability__do_delete_tags',
        'backend_api_resolvers_vulnerability__do_request_verification_vuln',
        'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
    )


def get_manager_actions() -> Tuple[str, ...]:
    """Actions that only client's project managers can perform."""
    return (
        'backend_api_resolvers_finding__do_handle_acceptation',
        'backend_api_resolvers_me__get_tags',
        'backend_api_resolvers_project__get_users',
        'backend_api_resolvers_project_resolve_reject_remove_project',
        'backend_api_resolvers_project_resolve_request_remove_project',
        'backend_api_resolvers_tag_resolve_tag',
        'backend_api_resolvers_user_resolve_edit_user',
        'backend_api_resolvers_user_resolve_grant_user_access',
        'backend_api_resolvers_user_resolve_remove_user_access',
        'backend_api_resolvers_user_resolve_user_list_projects',
        'backend_api_resolvers_user_resolve_user',
    )


def get_internal_manager_actions() -> Tuple[str, ...]:
    """Actions that only FluidAttacks's project managers can perform."""
    return (
        'backend_api_resolvers_alert_resolve_set_alert',
        'backend_api_resolvers_event__do_create_event',
        'backend_api_resolvers_project_resolve_create_project',
        'backend_api_resolvers_user_resolve_user_list_projects',
    )


def get_analyst_actions() -> Tuple[str, ...]:
    """Actions that only FluidAttacks's hackers can perform."""
    return (
        'backend_api_dataloaders_finding__get_analyst',
        'backend_api_dataloaders_finding__get_historic_state',
        'backend_api_dataloaders_finding__get_observations',
        'backend_api_resolvers_cache_resolve_invalidate_cache',
        'backend_api_resolvers_event__do_create_event',
        'backend_api_resolvers_event__do_remove_event_evidence',
        'backend_api_resolvers_event__do_solve_event',
        'backend_api_resolvers_event__do_update_event_evidence',
        'backend_api_resolvers_finding__do_create_draft',
        'backend_api_resolvers_finding__do_delete_finding',
        'backend_api_resolvers_finding__do_reject_draft',
        'backend_api_resolvers_finding__do_remove_evidence',
        'backend_api_resolvers_finding__do_submit_draft',
        'backend_api_resolvers_finding__do_update_description',
        'backend_api_resolvers_finding__do_update_evidence_description',
        'backend_api_resolvers_finding__do_update_evidence',
        'backend_api_resolvers_finding__do_update_severity',
        'backend_api_resolvers_finding__do_verify_finding',
        'backend_api_resolvers_project__get_drafts',
        'backend_api_resolvers_vulnerability__do_approve_vulnerability',
        'backend_api_resolvers_vulnerability__do_delete_vulnerability',
        'backend_api_resolvers_vulnerability__do_upload_file',
        'backend_api_resolvers_vulnerability__do_verify_request_vuln',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_analyst',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_last_analyst',
    )


def get_admin_actions() -> Tuple[str, ...]:
    """Actions that only platform admins can perform."""
    return (
        'backend_api_resolvers_cache_resolve_invalidate_cache',
        'backend_api_resolvers_finding__do_approve_draft',
        'backend_api_resolvers_internal_project_resolve_project_name',
        'backend_api_resolvers_project_resolve_add_all_project_access',
        'backend_api_resolvers_project_resolve_alive_projects',
        'backend_api_resolvers_project_resolve_create_project',
        'backend_api_resolvers_project_resolve_remove_all_project_access',
        'backend_api_resolvers_subscription__do_post_broadcast_message',
        'backend_api_resolvers_user_resolve_add_user',
    )


def list_actions() -> Tuple[str, ...]:
    all_actions = get_basic_actions() \
        + get_customer_actions() \
        + get_manager_actions() \
        + get_internal_manager_actions() \
        + get_analyst_actions() \
        + get_admin_actions()

    return tuple(set(all_actions))


def matches_permission(subject: str, role: str, action: str) -> bool:
    if action in get_basic_actions():
        matches = True
    elif action in get_customer_actions() \
            and role in ('admin', 'customer', 'customeradmin'):
        matches = True
    elif action in get_manager_actions() \
            and role in ('admin', 'customeradmin'):
        matches = True
    elif action in get_internal_manager_actions() \
            and role in ('admin', 'customer', 'customeradmin') \
            and subject.endswith('@fluidattacks.com'):
        matches = True
    elif action in get_analyst_actions():
        matches = role in ('admin', 'analyst')
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

    enforcer = CasbinEnforcer(
        model=get_perm_metamodel_path('group_level_async.conf'),
        adapter=adapter,
    )

    enforcer.fm.add_function('matchesPermission', matches_permission)

    return enforcer


def revoke_cached_subject_policies(subject: str) -> bool:
    """Revoke the cached policies for the provided subject."""
    cache_key: str = get_subject_cache_key(subject)

    # Delete the cache key from the cache
    cache.delete_pattern(f'*{cache_key}*')

    # Refresh the cache key as the user is probably going to use it soon :)
    get_cached_subject_policies(subject)

    return True
