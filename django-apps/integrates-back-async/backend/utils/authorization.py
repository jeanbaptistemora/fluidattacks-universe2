# Standard library
import contextlib
import os
from typing import Tuple

# Third party library
import rollbar
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


# Actions client's users can perform
CUSTOMER_ACTIONS: Tuple[str, ...] = (
    'backend_api_resolvers_alert_resolve_alert',
    'backend_api_resolvers_event__do_add_event_comment',
    'backend_api_resolvers_event__do_download_event_file',
    'backend_api_resolvers_event_resolve_event',
    'backend_api_resolvers_event_resolve_events',
    'backend_api_resolvers_finding__do_add_finding_comment',
    'backend_api_resolvers_finding_resolve_finding',
    'backend_api_resolvers_forces_resolve_forces_executions',
    'backend_api_resolvers_project__do_add_project_comment',
    'backend_api_resolvers_project__get_comments',
    'backend_api_resolvers_project__get_events',
    'backend_api_resolvers_project_resolve_project',
    'backend_api_resolvers_resource__do_download_file',
    'backend_api_resolvers_resource_resolve_resources',
    'backend_api_resolvers_vulnerability__do_request_verification_vuln',
    'backend_api_resolvers_finding__do_update_client_description',
    'backend_api_resolvers_project__do_add_tags',
    'backend_api_resolvers_project__do_remove_tag',
    'backend_api_resolvers_resource__do_add_environments',
    'backend_api_resolvers_resource__do_add_files',
    'backend_api_resolvers_resource__do_add_repositories',
    'backend_api_resolvers_resource__do_remove_files',
    'backend_api_resolvers_resource__do_update_environment',
    'backend_api_resolvers_resource__do_update_repository',
    'backend_api_resolvers_resource_resolve_add_resources',
    'backend_api_resolvers_vulnerability__do_delete_tags',
    'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
)


# Actions client's project managers can perform
CUSTOMERADMIN_ACTIONS: Tuple[str, ...] = (
    'backend_api_resolvers_alert_resolve_alert',
    'backend_api_resolvers_event__do_add_event_comment',
    'backend_api_resolvers_event__do_download_event_file',
    'backend_api_resolvers_event_resolve_event',
    'backend_api_resolvers_event_resolve_events',
    'backend_api_resolvers_finding__do_add_finding_comment',
    'backend_api_resolvers_finding_resolve_finding',
    'backend_api_resolvers_forces_resolve_forces_executions',
    'backend_api_resolvers_project__do_add_project_comment',
    'backend_api_resolvers_project__get_comments',
    'backend_api_resolvers_project__get_events',
    'backend_api_resolvers_project_resolve_project',
    'backend_api_resolvers_resource__do_download_file',
    'backend_api_resolvers_resource_resolve_resources',
    'backend_api_resolvers_vulnerability__do_request_verification_vuln',
    'backend_api_resolvers_finding__do_update_client_description',
    'backend_api_resolvers_project__do_add_tags',
    'backend_api_resolvers_project__do_remove_tag',
    'backend_api_resolvers_resource__do_add_environments',
    'backend_api_resolvers_resource__do_add_files',
    'backend_api_resolvers_resource__do_add_repositories',
    'backend_api_resolvers_resource__do_remove_files',
    'backend_api_resolvers_resource__do_update_environment',
    'backend_api_resolvers_resource__do_update_repository',
    'backend_api_resolvers_resource_resolve_add_resources',
    'backend_api_resolvers_vulnerability__do_delete_tags',
    'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
    'backend_api_resolvers_finding__do_handle_acceptation',
    'backend_api_resolvers_me__get_tags',
    'backend_api_resolvers_project__do_reject_remove_project',
    'backend_api_resolvers_project__do_request_remove_project',
    'backend_api_resolvers_project__get_users',
    'backend_api_resolvers_tag_resolve_tag',
    'backend_api_resolvers_user__do_edit_user',
    'backend_api_resolvers_user__do_grant_user_access',
    'backend_api_resolvers_user__do_remove_user_access',
    'backend_api_resolvers_user_resolve_user_list_projects',
    'backend_api_resolvers_user_resolve_user',
)


# Actions FluidAttacks's project managers can perform
INTERNAL_MANAGER_ACTIONS: Tuple[str, ...] = (
    'backend_api_resolvers_alert_resolve_alert',
    'backend_api_resolvers_event__do_add_event_comment',
    'backend_api_resolvers_event__do_download_event_file',
    'backend_api_resolvers_event_resolve_event',
    'backend_api_resolvers_event_resolve_events',
    'backend_api_resolvers_finding__do_add_finding_comment',
    'backend_api_resolvers_finding_resolve_finding',
    'backend_api_resolvers_forces_resolve_forces_executions',
    'backend_api_resolvers_project__do_add_project_comment',
    'backend_api_resolvers_project__get_comments',
    'backend_api_resolvers_project__get_events',
    'backend_api_resolvers_project_resolve_project',
    'backend_api_resolvers_resource__do_download_file',
    'backend_api_resolvers_resource_resolve_resources',
    'backend_api_resolvers_vulnerability__do_request_verification_vuln',
    'backend_api_resolvers_finding__do_update_client_description',
    'backend_api_resolvers_project__do_add_tags',
    'backend_api_resolvers_project__do_remove_tag',
    'backend_api_resolvers_resource__do_add_environments',
    'backend_api_resolvers_resource__do_add_files',
    'backend_api_resolvers_resource__do_add_repositories',
    'backend_api_resolvers_resource__do_remove_files',
    'backend_api_resolvers_resource__do_update_environment',
    'backend_api_resolvers_resource__do_update_repository',
    'backend_api_resolvers_resource_resolve_add_resources',
    'backend_api_resolvers_vulnerability__do_delete_tags',
    'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
    'backend_api_resolvers_finding__do_handle_acceptation',
    'backend_api_resolvers_me__get_tags',
    'backend_api_resolvers_project__do_reject_remove_project',
    'backend_api_resolvers_project__do_request_remove_project',
    'backend_api_resolvers_project__get_users',
    'backend_api_resolvers_tag_resolve_tag',
    'backend_api_resolvers_user__do_edit_user',
    'backend_api_resolvers_user__do_grant_user_access',
    'backend_api_resolvers_user__do_remove_user_access',
    'backend_api_resolvers_user_resolve_user_list_projects',
    'backend_api_resolvers_user_resolve_user',
    'backend_api_resolvers_alert_resolve_set_alert',
    'backend_api_resolvers_event__do_create_event',
    'backend_api_resolvers_project__do_create_project',
    'backend_api_resolvers_user_resolve_user_list_projects',
)


# Actions FluidAttacks's hackers can perform
ANALYST_ACTIONS: Tuple[str, ...] = (
    'backend_api_resolvers_alert_resolve_alert',
    'backend_api_resolvers_event__do_add_event_comment',
    'backend_api_resolvers_event__do_download_event_file',
    'backend_api_resolvers_event_resolve_event',
    'backend_api_resolvers_event_resolve_events',
    'backend_api_resolvers_finding__do_add_finding_comment',
    'backend_api_resolvers_finding_resolve_finding',
    'backend_api_resolvers_forces_resolve_forces_executions',
    'backend_api_resolvers_project__do_add_project_comment',
    'backend_api_resolvers_project__get_comments',
    'backend_api_resolvers_project__get_events',
    'backend_api_resolvers_project_resolve_project',
    'backend_api_resolvers_resource__do_download_file',
    'backend_api_resolvers_resource_resolve_resources',
    'backend_api_resolvers_vulnerability__do_request_verification_vuln',
    'backend_api_dataloaders_finding__get_analyst',
    'backend_api_dataloaders_finding__get_historic_state',
    'backend_api_dataloaders_finding__get_observations',
    'backend_api_dataloaders_finding__get_pending_vulns',
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
    'backend_api_resolvers_project__get_drafts',
    'backend_api_resolvers_vulnerability__do_approve_vulnerability',
    'backend_api_resolvers_vulnerability__do_delete_vulnerability',
    'backend_api_resolvers_vulnerability__do_upload_file',
    'backend_api_resolvers_vulnerability__do_verify_request_vuln',
    'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_analyst',
    'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_last_analyst',
)


# Actions Administrators can perform
ADMIN_ACTIONS: Tuple[str, ...] = (
    'backend_api_resolvers_alert_resolve_alert',
    'backend_api_resolvers_event__do_add_event_comment',
    'backend_api_resolvers_event__do_download_event_file',
    'backend_api_resolvers_event_resolve_event',
    'backend_api_resolvers_event_resolve_events',
    'backend_api_resolvers_finding__do_add_finding_comment',
    'backend_api_resolvers_finding_resolve_finding',
    'backend_api_resolvers_forces_resolve_forces_executions',
    'backend_api_resolvers_project__do_add_project_comment',
    'backend_api_resolvers_project__get_comments',
    'backend_api_resolvers_project__get_events',
    'backend_api_resolvers_project_resolve_project',
    'backend_api_resolvers_resource__do_download_file',
    'backend_api_resolvers_resource_resolve_resources',
    'backend_api_resolvers_vulnerability__do_request_verification_vuln',
    'backend_api_resolvers_project__do_add_tags',
    'backend_api_resolvers_project__do_remove_tag',
    'backend_api_resolvers_resource__do_add_environments',
    'backend_api_resolvers_resource__do_add_files',
    'backend_api_resolvers_resource__do_add_repositories',
    'backend_api_resolvers_resource__do_remove_files',
    'backend_api_resolvers_resource__do_update_environment',
    'backend_api_resolvers_resource__do_update_repository',
    'backend_api_resolvers_resource_resolve_add_resources',
    'backend_api_resolvers_me__get_tags',
    'backend_api_resolvers_project__do_reject_remove_project',
    'backend_api_resolvers_project__do_request_remove_project',
    'backend_api_resolvers_project__get_users',
    'backend_api_resolvers_tag_resolve_tag',
    'backend_api_resolvers_user__do_edit_user',
    'backend_api_resolvers_user__do_grant_user_access',
    'backend_api_resolvers_user__do_remove_user_access',
    'backend_api_resolvers_user_resolve_user_list_projects',
    'backend_api_resolvers_user_resolve_user',
    'backend_api_resolvers_alert_resolve_set_alert',
    'backend_api_resolvers_event__do_create_event',
    'backend_api_resolvers_project__do_create_project',
    'backend_api_resolvers_user_resolve_user_list_projects',
    'backend_api_dataloaders_finding__get_analyst',
    'backend_api_dataloaders_finding__get_historic_state',
    'backend_api_dataloaders_finding__get_observations',
    'backend_api_dataloaders_finding__get_pending_vulns',
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
    'backend_api_resolvers_project__get_drafts',
    'backend_api_resolvers_vulnerability__do_approve_vulnerability',
    'backend_api_resolvers_vulnerability__do_delete_vulnerability',
    'backend_api_resolvers_vulnerability__do_upload_file',
    'backend_api_resolvers_vulnerability__do_verify_request_vuln',
    'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_analyst',
    'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_last_analyst',
    'backend_api_resolvers_cache_resolve_invalidate_cache',
    'backend_api_resolvers_finding__do_approve_draft',
    'backend_api_resolvers_internal_project_resolve_project_name',
    'backend_api_resolvers_project__do_add_all_project_access',
    'backend_api_resolvers_project__do_create_project',
    'backend_api_resolvers_project__do_remove_all_project_access',
    'backend_api_resolvers_project_resolve_alive_projects',
    'backend_api_resolvers_subscription__do_post_broadcast_message',
    'backend_api_resolvers_user__do_add_user',
    'backend_api_resolvers_user__do_grant_user_access_internal_roles',
)


ALL_ACTIONS: Tuple[str, ...] = tuple(set((
    *CUSTOMER_ACTIONS,
    *CUSTOMERADMIN_ACTIONS,
    *INTERNAL_MANAGER_ACTIONS,
    *ANALYST_ACTIONS,
    *ADMIN_ACTIONS,
)))


def matches_permission(subject: str, role: str, action: str) -> bool:
    role_actions = {
        'admin': ADMIN_ACTIONS,
        'analyst': ANALYST_ACTIONS,
        'customer': CUSTOMER_ACTIONS,
        'customeradmin': CUSTOMERADMIN_ACTIONS,
        'internal_manager': INTERNAL_MANAGER_ACTIONS,
    }
    if role in role_actions:
        matches = action in role_actions[role]
    else:
        matches = False
        rollbar.report_message(
            'No actions set for role',
            level='error', extra_data={role, subject})

    return matches


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
