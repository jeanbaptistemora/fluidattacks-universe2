# Standard library
import contextlib
from typing import (
    Callable,
    Coroutine,
    Dict,
    List,
    Set,
    Tuple,
)

# Third party library
import rollbar
from django.core.cache import cache
from rediscluster.nodemanager import RedisClusterException
from backend.dal import (
    project as project_dal,
    user as user_dal,
)

# Map(role_level -> Map(role_name -> tags))
ROLES: Dict[str, Dict[str, List[str]]] = dict(
    group_level=dict(
        analyst=['drills'],
        closer=['drills'],
        customer=[],
        customeradmin=[],
        group_manager=['drills'],
        reviewer=['drills'],
    ),
    user_level=dict(
        admin=[],
        customer=[],
        customeradmin=[],
        internal_manager=['drills'],
    ),
)

# Map(service -> feature)
SERVICE_ATTRIBUTES: Dict[str, Set[str]] = dict(
    drills_black={
        'is_fluidattacks_customer',
        'must_only_have_fluidattacks_hackers',
    },
    drills_white={
        'is_fluidattacks_customer',
        'must_only_have_fluidattacks_hackers',
    },
    forces={
        'is_fluidattacks_customer',
        'must_only_have_fluidattacks_hackers',
    },
    integrates=set(),
)


def get_subject_cache_key(subject: str) -> str:
    return f'authorization.subject.{subject.lower().encode().hex()}'


def get_group_cache_key(group: str) -> str:
    return f'authorization.group.{group.lower().encode().hex()}'


def get_cached_subject_policies(subject: str):
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


def get_cached_group_service_attributes_policies(group: str):
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


# Actions client's users can perform
CUSTOMER_ACTIONS: Tuple[str, ...] = (
    'backend_api_resolvers_alert_resolve_alert',
    'backend_api_resolvers_event__do_add_event_comment',
    'backend_api_resolvers_event__do_download_event_file',
    'backend_api_resolvers_event_resolve_event',
    'backend_api_resolvers_event_resolve_events',
    'backend_api_resolvers_finding__do_add_finding_comment',
    'backend_api_resolvers_finding__do_update_client_description',
    'backend_api_resolvers_finding_resolve_finding',
    'backend_api_resolvers_forces_resolve_forces_executions',
    'backend_api_resolvers_internal_project_resolve_project_name',
    'backend_api_resolvers_project__do_add_project_comment',
    'backend_api_resolvers_project__do_add_tags',
    'backend_api_resolvers_project__do_create_project',
    'backend_api_resolvers_project__do_remove_tag',
    'backend_api_resolvers_project__get_comments',
    'backend_api_resolvers_project__get_events',
    'backend_api_resolvers_project_resolve_project',
    'backend_api_resolvers_resource__do_add_environments',
    'backend_api_resolvers_resource__do_add_files',
    'backend_api_resolvers_resource__do_add_repositories',
    'backend_api_resolvers_resource__do_download_file',
    'backend_api_resolvers_resource__do_remove_files',
    'backend_api_resolvers_resource__do_update_environment',
    'backend_api_resolvers_resource__do_update_repository',
    'backend_api_resolvers_resource_resolve_add_resources',
    'backend_api_resolvers_resource_resolve_resources',
    'backend_api_resolvers_vulnerability__do_delete_tags',
    'backend_api_resolvers_vulnerability__do_request_verification_vuln',
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
    'backend_api_resolvers_finding__do_handle_acceptation',
    'backend_api_resolvers_finding__do_update_client_description',
    'backend_api_resolvers_finding_resolve_finding',
    'backend_api_resolvers_forces_resolve_forces_executions',
    'backend_api_resolvers_internal_project_resolve_project_name',
    'backend_api_resolvers_me__get_tags',
    'backend_api_resolvers_project__do_add_project_comment',
    'backend_api_resolvers_project__do_add_tags',
    'backend_api_resolvers_project__do_create_project',
    'backend_api_resolvers_project__do_reject_remove_project',
    'backend_api_resolvers_project__do_remove_tag',
    'backend_api_resolvers_project__do_request_remove_project',
    'backend_api_resolvers_project__get_comments',
    'backend_api_resolvers_project__get_events',
    'backend_api_resolvers_project__get_users',
    'backend_api_resolvers_project_resolve_project',
    'backend_api_resolvers_resource__do_add_environments',
    'backend_api_resolvers_resource__do_add_files',
    'backend_api_resolvers_resource__do_add_repositories',
    'backend_api_resolvers_resource__do_download_file',
    'backend_api_resolvers_resource__do_remove_files',
    'backend_api_resolvers_resource__do_update_environment',
    'backend_api_resolvers_resource__do_update_repository',
    'backend_api_resolvers_resource_resolve_add_resources',
    'backend_api_resolvers_resource_resolve_resources',
    'backend_api_resolvers_tag_resolve_tag',
    'backend_api_resolvers_user__do_edit_user',
    'backend_api_resolvers_user__do_grant_user_access',
    'backend_api_resolvers_user__do_remove_user_access',
    'backend_api_resolvers_user_resolve_user_list_projects',
    'backend_api_resolvers_user_resolve_user',
    'backend_api_resolvers_vulnerability__do_delete_tags',
    'backend_api_resolvers_vulnerability__do_request_verification_vuln',
    'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
    'grant_user_level_role:customer',
    'grant_user_level_role:customeradmin',
    'grant_group_level_role:analyst',
    'grant_group_level_role:customer',
    'grant_group_level_role:customeradmin',
)


# Actions FluidAttacks's project managers can perform on group level
GROUP_MANAGER_ACTIONS: Tuple[str, ...] = (
    'backend_api_resolvers_alert_resolve_alert',
    'backend_api_resolvers_alert_resolve_set_alert',
    'backend_api_resolvers_event__do_add_event_comment',
    'backend_api_resolvers_event__do_create_event',
    'backend_api_resolvers_event__do_download_event_file',
    'backend_api_resolvers_event__do_solve_event',
    'backend_api_resolvers_event_resolve_event',
    'backend_api_resolvers_event_resolve_events',
    'backend_api_resolvers_finding__do_add_finding_comment',
    'backend_api_resolvers_finding__do_handle_acceptation',
    'backend_api_resolvers_finding__do_update_client_description',
    'backend_api_resolvers_finding_resolve_finding',
    'backend_api_resolvers_forces_resolve_forces_executions',
    'backend_api_resolvers_project__do_add_project_comment',
    'backend_api_resolvers_project__do_add_tags',
    'backend_api_resolvers_project__do_reject_remove_project',
    'backend_api_resolvers_project__do_remove_tag',
    'backend_api_resolvers_project__do_request_remove_project',
    'backend_api_resolvers_project__get_comments',
    'backend_api_resolvers_project__get_drafts',
    'backend_api_resolvers_project__get_events',
    'backend_api_resolvers_project__get_users',
    'backend_api_resolvers_project_resolve_project',
    'backend_api_resolvers_resource__do_add_environments',
    'backend_api_resolvers_resource__do_add_files',
    'backend_api_resolvers_resource__do_add_repositories',
    'backend_api_resolvers_resource__do_download_file',
    'backend_api_resolvers_resource__do_remove_files',
    'backend_api_resolvers_resource__do_update_environment',
    'backend_api_resolvers_resource__do_update_repository',
    'backend_api_resolvers_resource_resolve_add_resources',
    'backend_api_resolvers_resource_resolve_resources',
    'backend_api_resolvers_user__do_edit_user',
    'backend_api_resolvers_user__do_grant_user_access',
    'backend_api_resolvers_user__do_remove_user_access',
    'backend_api_resolvers_user_resolve_user',
    'backend_api_resolvers_vulnerability__do_delete_tags',
    'backend_api_resolvers_vulnerability__do_request_verification_vuln',
    'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
    'grant_user_level_role:customer',
    'grant_user_level_role:customeradmin',
    'grant_group_level_role:analyst',
    'grant_group_level_role:customer',
    'grant_group_level_role:customeradmin',
)


# Actions FluidAttacks's project managers can perform on user level
INTERNAL_MANAGER_ACTIONS: Tuple[str, ...] = (
    'backend_api_resolvers_internal_project_resolve_project_name',
    'backend_api_resolvers_me__get_tags',
    'backend_api_resolvers_project__do_create_project',
    'backend_api_resolvers_tag_resolve_tag',
    'backend_api_resolvers_user_resolve_user_list_projects',
)


# Actions FluidAttacks's hackers can perform
ANALYST_ACTIONS: Tuple[str, ...] = (
    'backend_api_resolvers_alert_resolve_alert',
    'backend_api_resolvers_cache_resolve_invalidate_cache',
    'backend_api_resolvers_event__do_add_event_comment',
    'backend_api_resolvers_event__do_create_event',
    'backend_api_resolvers_event__do_download_event_file',
    'backend_api_resolvers_event__do_remove_event_evidence',
    'backend_api_resolvers_event__do_solve_event',
    'backend_api_resolvers_event__do_update_event_evidence',
    'backend_api_resolvers_event_resolve_event',
    'backend_api_resolvers_event_resolve_events',
    'backend_api_resolvers_finding__do_add_finding_comment',
    'backend_api_resolvers_finding__do_create_draft',
    'backend_api_resolvers_finding__do_delete_finding',
    'backend_api_resolvers_finding__do_reject_draft',
    'backend_api_resolvers_finding__do_remove_evidence',
    'backend_api_resolvers_finding__do_submit_draft',
    'backend_api_resolvers_finding__do_update_description',
    'backend_api_resolvers_finding__do_update_evidence_description',
    'backend_api_resolvers_finding__do_update_evidence',
    'backend_api_resolvers_finding__do_update_severity',
    'backend_api_resolvers_finding__get_analyst',
    'backend_api_resolvers_finding__get_historic_state',
    'backend_api_resolvers_finding__get_observations',
    'backend_api_resolvers_finding__get_pending_vulns',
    'backend_api_resolvers_finding_resolve_finding',
    'backend_api_resolvers_forces_resolve_forces_executions',
    'backend_api_resolvers_internal_project_resolve_project_name',
    'backend_api_resolvers_project__do_add_project_comment',
    'backend_api_resolvers_project__do_create_project',
    'backend_api_resolvers_project__get_comments',
    'backend_api_resolvers_project__get_drafts',
    'backend_api_resolvers_project__get_events',
    'backend_api_resolvers_project_resolve_project',
    'backend_api_resolvers_resource__do_download_file',
    'backend_api_resolvers_resource_resolve_resources',
    'backend_api_resolvers_vulnerability__do_approve_vulnerability',
    'backend_api_resolvers_vulnerability__do_delete_vulnerability',
    'backend_api_resolvers_vulnerability__do_request_verification_vuln',
    'backend_api_resolvers_vulnerability__do_upload_file',
    'backend_api_resolvers_vulnerability__do_verify_request_vuln',
    'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_analyst',
    'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_last_analyst',
)


# Actions Administrators can perform
ADMIN_ACTIONS: Tuple[str, ...] = (
    'backend_api_resolvers_alert_resolve_alert',
    'backend_api_resolvers_alert_resolve_set_alert',
    'backend_api_resolvers_cache_resolve_invalidate_cache',
    'backend_api_resolvers_event__do_add_event_comment',
    'backend_api_resolvers_event__do_create_event',
    'backend_api_resolvers_event__do_download_event_file',
    'backend_api_resolvers_event__do_remove_event_evidence',
    'backend_api_resolvers_event__do_solve_event',
    'backend_api_resolvers_event__do_update_event_evidence',
    'backend_api_resolvers_event_resolve_event',
    'backend_api_resolvers_event_resolve_events',
    'backend_api_resolvers_finding__do_add_finding_comment',
    'backend_api_resolvers_finding__do_approve_draft',
    'backend_api_resolvers_finding__do_create_draft',
    'backend_api_resolvers_finding__do_delete_finding',
    'backend_api_resolvers_finding__do_reject_draft',
    'backend_api_resolvers_finding__do_remove_evidence',
    'backend_api_resolvers_finding__do_submit_draft',
    'backend_api_resolvers_finding__do_update_description',
    'backend_api_resolvers_finding__do_update_evidence_description',
    'backend_api_resolvers_finding__do_update_evidence',
    'backend_api_resolvers_finding__do_update_severity',
    'backend_api_resolvers_finding__get_analyst',
    'backend_api_resolvers_finding__get_historic_state',
    'backend_api_resolvers_finding__get_observations',
    'backend_api_resolvers_finding__get_pending_vulns',
    'backend_api_resolvers_finding_resolve_finding',
    'backend_api_resolvers_forces_resolve_forces_executions',
    'backend_api_resolvers_internal_project_resolve_project_name',
    'backend_api_resolvers_me__get_tags',
    'backend_api_resolvers_project__do_add_all_project_access',
    'backend_api_resolvers_project__do_add_project_comment',
    'backend_api_resolvers_project__do_add_tags',
    'backend_api_resolvers_project__do_create_project',
    'backend_api_resolvers_project__do_reject_remove_project',
    'backend_api_resolvers_project__do_remove_all_project_access',
    'backend_api_resolvers_project__do_remove_tag',
    'backend_api_resolvers_project__do_request_remove_project',
    'backend_api_resolvers_project__get_comments',
    'backend_api_resolvers_project__get_drafts',
    'backend_api_resolvers_project__get_events',
    'backend_api_resolvers_project__get_users',
    'backend_api_resolvers_project_resolve_alive_projects',
    'backend_api_resolvers_project_resolve_project',
    'backend_api_resolvers_resource__do_add_environments',
    'backend_api_resolvers_resource__do_add_files',
    'backend_api_resolvers_resource__do_add_repositories',
    'backend_api_resolvers_resource__do_download_file',
    'backend_api_resolvers_resource__do_remove_files',
    'backend_api_resolvers_resource__do_update_environment',
    'backend_api_resolvers_resource__do_update_repository',
    'backend_api_resolvers_resource_resolve_add_resources',
    'backend_api_resolvers_resource_resolve_resources',
    'backend_api_resolvers_subscription__do_post_broadcast_message',
    'backend_api_resolvers_tag_resolve_tag',
    'backend_api_resolvers_user__do_add_user',
    'backend_api_resolvers_user__do_edit_user',
    'backend_api_resolvers_user__do_grant_user_access',
    'backend_api_resolvers_user__do_remove_user_access',
    'backend_api_resolvers_user_resolve_user_list_projects',
    'backend_api_resolvers_user_resolve_user',
    'backend_api_resolvers_vulnerability__do_approve_vulnerability',
    'backend_api_resolvers_vulnerability__do_delete_vulnerability',
    'backend_api_resolvers_vulnerability__do_request_verification_vuln',
    'backend_api_resolvers_vulnerability__do_upload_file',
    'backend_api_resolvers_vulnerability__do_verify_request_vuln',
    'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_analyst',
    'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_last_analyst',
    'grant_user_level_role:admin',
    'grant_user_level_role:customer',
    'grant_user_level_role:customeradmin',
    'grant_user_level_role:internal_manager',
    'grant_group_level_role:analyst',
    'grant_group_level_role:closer',
    'grant_group_level_role:customer',
    'grant_group_level_role:customeradmin',
    'grant_group_level_role:group_manager',
    'grant_group_level_role:reviewer',
)


ALL_ACTIONS: Tuple[str, ...] = tuple(set((
    *CUSTOMER_ACTIONS,
    *CUSTOMERADMIN_ACTIONS,
    *GROUP_MANAGER_ACTIONS,
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
        'group_manager': GROUP_MANAGER_ACTIONS,
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


def get_group_level_roles_with_tag(tag: str) -> Set[str]:
    return {role for role, tags in ROLES['group_level'].items() if tag in tags}


def get_user_level_enforcer(subject: str) -> Callable[[str, str, str], Coroutine]:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)

    async def enforcer(r_subject: str, r_object: str, r_action: str) -> bool:
        should_grant_access: bool = any(
            p_level == 'user'
            and r_subject == p_subject
            and r_object == p_object
            and matches_permission(r_subject, p_role, r_action)
            for p_level, p_subject, p_object, p_role in policies
        )

        return should_grant_access

    return enforcer


def get_group_level_enforcer(subject: str) -> Callable[[str, str, str], Coroutine]:
    """Return a filtered group-level authorization for the provided subject."""
    policies = get_cached_subject_policies(subject)

    async def enforcer(r_subject: str, r_object: str, r_action: str) -> bool:
        should_grant_access: bool = any(
            r_subject == p_subject
            and ((p_level == 'user' and p_role == 'admin') or
                 (p_level == 'group' and r_object == p_object))
            and matches_permission(r_subject, p_role, r_action)
            for p_level, p_subject, p_object, p_role in policies
        )

        return should_grant_access

    return enforcer


def get_group_service_attributes_enforcer(group: str) -> Callable[[str, str], Coroutine]:
    """Return a filtered group authorization for the provided group."""
    policies = get_cached_group_service_attributes_policies(group)

    async def enforcer(r_group: str, r_action: str) -> bool:
        should_grant_access: bool = any(
            r_group == p_group
            and r_action in SERVICE_ATTRIBUTES[p_service]
            for p_group, p_service in policies
        )

        return should_grant_access

    return enforcer


async def get_user_level_roles_a_user_can_grant(
    *,
    requester_email: str,
) -> Tuple[str, ...]:
    """Return a tuple of roles that users can grant based on their role."""
    enforcer = get_user_level_enforcer(requester_email)

    roles_the_user_can_grant: Tuple[str, ...] = tuple([
        role
        for role in ROLES['user_level']
        if await enforcer(
            requester_email, 'self', f'grant_user_level_role:{role}'
        )
    ])

    return roles_the_user_can_grant


async def get_group_level_roles_a_user_can_grant(
    *,
    group: str,
    requester_email: str,
) -> Tuple[str, ...]:
    """Return a tuple of roles that users can grant based on their role."""
    enforcer = get_group_level_enforcer(requester_email)

    roles_the_user_can_grant: Tuple[str, ...] = tuple([
        role
        for role in ROLES['group_level']
        if await enforcer(
            requester_email, group, f'grant_group_level_role:{role}'
        )
    ])

    return roles_the_user_can_grant


def get_group_access_enforcer() -> Callable[[dict, str], Coroutine]:

    # If you are going to create a new enforcer do not follow this pattern
    #   use a policy based enforcer
    # see: get_user_level_enforcer or get_group_level_enforcer for examples
    async def enforcer(r_data: dict, r_object: str) -> bool:
        should_grant_access: bool = \
            r_data['role'] == 'admin' \
            or r_object.lower() in r_data['subscribed_projects']

        return should_grant_access

    return enforcer


def revoke_cached_subject_policies(subject: str) -> bool:
    """Revoke the cached policies for the provided subject."""
    cache_key: str = get_subject_cache_key(subject)

    # Delete the cache key from the cache
    cache.delete_pattern(f'*{cache_key}*')

    # Refresh the cache key as the user is probably going to use it soon :)
    get_cached_subject_policies(subject)

    return True
