# Standard library
from typing import (
    Dict,
    Set,
)


# Map(role_name -> Map(actions|tags -> definition))
GROUP_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            'backend_api_resolvers_alert_resolve_alert',
            'backend_api_resolvers_alert_resolve_set_alert',
            'backend_api_resolvers_analytics__get_group_document',
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
            'backend_api_resolvers_organization__do_move_group_organization',
            'backend_api_resolvers_project__do_add_project_comment',
            'backend_api_resolvers_project__do_add_tags',
            'backend_api_resolvers_project__do_edit_group',
            'backend_api_resolvers_project__do_reject_remove_project',
            'backend_api_resolvers_project__do_remove_tag',
            'backend_api_resolvers_project__get_bill',
            'backend_api_resolvers_project__get_comments',
            'backend_api_resolvers_project__get_drafts',
            'backend_api_resolvers_project__get_events',
            'backend_api_resolvers_project__get_service_attributes',
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
            'backend_api_resolvers_user_resolve_for_group',
            'backend_api_resolvers_vulnerability__do_approve_vulnerability',
            'backend_api_resolvers_vulnerability__do_delete_vulnerability',
            'backend_api_resolvers_vulnerability__do_download_vuln_file',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_upload_file',
            'backend_api_resolvers_vulnerability__do_verify_request_vuln',
            ('backend_api_resolvers_vulnerability_resolve_'
                'vulnerability_resolve_analyst'),
            ('backend_api_resolvers_vulnerability_resolve_'
                'vulnerability_resolve_last_analyst'),
            'grant_group_level_role:analyst',
            'grant_group_level_role:closer',
            'grant_group_level_role:customer',
            'grant_group_level_role:customeradmin',
            'grant_group_level_role:executive',
            'grant_group_level_role:group_manager',
            'grant_group_level_role:resourcer',
            'grant_group_level_role:reviewer',
        },
        tags=set(),
    ),
    analyst=dict(
        actions={
            'backend_api_resolvers_alert_resolve_alert',
            'backend_api_resolvers_analytics__get_group_document',
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
            'backend_api_resolvers_project__do_add_project_comment',
            'backend_api_resolvers_project__get_comments',
            'backend_api_resolvers_project__get_drafts',
            'backend_api_resolvers_project__get_events',
            'backend_api_resolvers_project__get_service_attributes',
            'backend_api_resolvers_project_resolve_project',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_resource_resolve_resources',
            'backend_api_resolvers_vulnerability__do_approve_vulnerability',
            'backend_api_resolvers_vulnerability__do_delete_vulnerability',
            'backend_api_resolvers_vulnerability__do_download_vuln_file',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_upload_file',
            'backend_api_resolvers_vulnerability__do_verify_request_vuln',
            ('backend_api_resolvers_vulnerability_resolve_'
                'vulnerability_resolve_analyst'),
            ('backend_api_resolvers_vulnerability_resolve_'
                'vulnerability_resolve_last_analyst'),
        },
        tags={
            'drills',
        },
    ),
    closer=dict(
        actions={
            'backend_api_resolvers_alert_resolve_alert',
            'backend_api_resolvers_analytics__get_group_document',
            'backend_api_resolvers_event__do_add_event_comment',
            'backend_api_resolvers_event__do_create_event',
            'backend_api_resolvers_event__do_download_event_file',
            'backend_api_resolvers_event_resolve_event',
            'backend_api_resolvers_event_resolve_events',
            'backend_api_resolvers_finding__do_add_finding_comment',
            'backend_api_resolvers_finding__do_update_description',
            'backend_api_resolvers_finding__do_update_evidence_description',
            'backend_api_resolvers_finding__do_update_evidence',
            'backend_api_resolvers_finding__get_analyst',
            'backend_api_resolvers_finding__get_historic_state',
            'backend_api_resolvers_finding__get_pending_vulns',
            'backend_api_resolvers_finding_resolve_finding',
            'backend_api_resolvers_forces_resolve_forces_executions',
            'backend_api_resolvers_project__get_comments',
            'backend_api_resolvers_project__get_events',
            'backend_api_resolvers_project__get_service_attributes',
            'backend_api_resolvers_project_resolve_project',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_resource_resolve_resources',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_download_vuln_file',
            'backend_api_resolvers_vulnerability__do_upload_file',
            'backend_api_resolvers_vulnerability__do_verify_request_vuln',
            ('backend_api_resolvers_vulnerability_resolve_'
                'vulnerability_resolve_analyst'),
            ('backend_api_resolvers_vulnerability_resolve_'
                'vulnerability_resolve_last_analyst'),
        },
        tags={
            'drills',
        },
    ),
    customer=dict(
        actions={
            'backend_api_resolvers_alert_resolve_alert',
            'backend_api_resolvers_analytics__get_group_document',
            'backend_api_resolvers_event__do_add_event_comment',
            'backend_api_resolvers_event__do_download_event_file',
            'backend_api_resolvers_event_resolve_event',
            'backend_api_resolvers_event_resolve_events',
            'backend_api_resolvers_finding__do_add_finding_comment',
            'backend_api_resolvers_finding__do_update_client_description',
            'backend_api_resolvers_finding__get_pending_vulns',
            'backend_api_resolvers_finding_resolve_finding',
            'backend_api_resolvers_forces_resolve_forces_executions',
            'backend_api_resolvers_project__do_add_project_comment',
            'backend_api_resolvers_project__do_add_tags',
            'backend_api_resolvers_project__do_remove_tag',
            'backend_api_resolvers_project__get_bill',
            'backend_api_resolvers_project__get_comments',
            'backend_api_resolvers_project__get_events',
            'backend_api_resolvers_project__get_service_attributes',
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
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
        },
        tags=set(),
    ),
    customeradmin=dict(
        actions={
            'backend_api_resolvers_alert_resolve_alert',
            'backend_api_resolvers_analytics__get_group_document',
            'backend_api_resolvers_event__do_add_event_comment',
            'backend_api_resolvers_event__do_download_event_file',
            'backend_api_resolvers_event_resolve_event',
            'backend_api_resolvers_event_resolve_events',
            'backend_api_resolvers_finding__do_add_finding_comment',
            'backend_api_resolvers_finding__do_handle_acceptation',
            'backend_api_resolvers_finding__do_update_client_description',
            'backend_api_resolvers_finding__get_pending_vulns',
            'backend_api_resolvers_finding_resolve_finding',
            'backend_api_resolvers_forces_resolve_forces_executions',
            'backend_api_resolvers_organization__do_move_group_organization',
            'backend_api_resolvers_project__do_add_project_comment',
            'backend_api_resolvers_project__do_add_tags',
            'backend_api_resolvers_project__do_edit_group',
            'backend_api_resolvers_project__do_reject_remove_project',
            'backend_api_resolvers_project__do_remove_tag',
            'backend_api_resolvers_project__get_bill',
            'backend_api_resolvers_project__get_comments',
            'backend_api_resolvers_project__get_events',
            'backend_api_resolvers_project__get_service_attributes',
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
            'backend_api_resolvers_user_resolve_for_group',
            'backend_api_resolvers_vulnerability__do_delete_tags',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
            'grant_user_level_role:customer',
            'grant_group_level_role:customer',
            'grant_group_level_role:customeradmin',
            'grant_group_level_role:executive',
        },
        tags=set(),
    ),
    executive=dict(
        actions={
            'backend_api_resolvers_alert_resolve_alert',
            'backend_api_resolvers_analytics__get_group_document',
            'backend_api_resolvers_event__do_add_event_comment',
            'backend_api_resolvers_event__do_download_event_file',
            'backend_api_resolvers_event_resolve_event',
            'backend_api_resolvers_event_resolve_events',
            'backend_api_resolvers_finding__do_add_finding_comment',
            'backend_api_resolvers_finding__do_update_client_description',
            'backend_api_resolvers_finding__get_pending_vulns',
            'backend_api_resolvers_finding_resolve_finding',
            'backend_api_resolvers_forces_resolve_forces_executions',
            'backend_api_resolvers_project__do_add_project_comment',
            'backend_api_resolvers_project__do_add_tags',
            'backend_api_resolvers_project__do_remove_tag',
            'backend_api_resolvers_project__get_comments',
            'backend_api_resolvers_project__get_events',
            'backend_api_resolvers_project__get_service_attributes',
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
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
        },
        tags=set()
    ),
    group_manager=dict(
        actions={
            'backend_api_resolvers_alert_resolve_alert',
            'backend_api_resolvers_alert_resolve_set_alert',
            'backend_api_resolvers_analytics__get_group_document',
            'backend_api_resolvers_event__do_add_event_comment',
            'backend_api_resolvers_event__do_create_event',
            'backend_api_resolvers_event__do_download_event_file',
            'backend_api_resolvers_event__do_solve_event',
            'backend_api_resolvers_event_resolve_event',
            'backend_api_resolvers_event_resolve_events',
            'backend_api_resolvers_finding__do_add_finding_comment',
            'backend_api_resolvers_finding__do_handle_acceptation',
            'backend_api_resolvers_finding__do_update_client_description',
            'backend_api_resolvers_finding__get_analyst',
            'backend_api_resolvers_finding__get_observations',
            'backend_api_resolvers_finding__get_pending_vulns',
            'backend_api_resolvers_finding_resolve_finding',
            'backend_api_resolvers_forces_resolve_forces_executions',
            'backend_api_resolvers_organization__do_move_group_organization',
            'backend_api_resolvers_project__do_add_project_comment',
            'backend_api_resolvers_project__do_add_tags',
            'backend_api_resolvers_project__do_edit_group',
            'backend_api_resolvers_project__do_reject_remove_project',
            'backend_api_resolvers_project__do_remove_tag',
            'backend_api_resolvers_project__get_bill',
            'backend_api_resolvers_project__get_comments',
            'backend_api_resolvers_project__get_drafts',
            'backend_api_resolvers_project__get_events',
            'backend_api_resolvers_project__get_service_attributes',
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
            'backend_api_resolvers_user_resolve_for_group',
            'backend_api_resolvers_vulnerability__do_delete_tags',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
            ('backend_api_resolvers_vulnerability_resolve_'
                'vulnerability_resolve_analyst'),
            ('backend_api_resolvers_vulnerability_resolve_'
                'vulnerability_resolve_last_analyst'),
            'grant_group_level_role:analyst',
            'grant_group_level_role:closer',
            'grant_user_level_role:customer',
            'grant_group_level_role:customer',
            'grant_group_level_role:customeradmin',
            'grant_group_level_role:executive',
            'grant_group_level_role:group_manager',
            'grant_group_level_role:reviewer',
            'grant_group_level_role:resourcer',
        },
        tags=set(),
    ),
    resourcer=dict(
        actions={
            'backend_api_resolvers_alert_resolve_alert',
            'backend_api_resolvers_analytics__get_group_document',
            'backend_api_resolvers_event__do_add_event_comment',
            'backend_api_resolvers_event__do_create_event',
            'backend_api_resolvers_event__do_download_event_file',
            'backend_api_resolvers_event_resolve_event',
            'backend_api_resolvers_event_resolve_events',
            'backend_api_resolvers_event__do_solve_event',
            'backend_api_resolvers_finding_resolve_finding',
            'backend_api_resolvers_forces_resolve_forces_executions',
            'backend_api_resolvers_project__get_comments',
            'backend_api_resolvers_project__get_events',
            'backend_api_resolvers_project__get_service_attributes',
            'backend_api_resolvers_project_resolve_project',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_resource_resolve_resources',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
        },
        tags={
            'drills',
        },
    ),
    reviewer=dict(
        actions={
            'backend_api_resolvers_alert_resolve_alert',
            'backend_api_resolvers_analytics__get_group_document',
            'backend_api_resolvers_event__do_add_event_comment',
            'backend_api_resolvers_event__do_download_event_file',
            'backend_api_resolvers_event_resolve_event',
            'backend_api_resolvers_event_resolve_events',
            'backend_api_resolvers_finding__do_add_finding_comment',
            'backend_api_resolvers_finding__do_approve_draft',
            'backend_api_resolvers_finding__do_delete_finding',
            'backend_api_resolvers_finding__do_reject_draft',
            'backend_api_resolvers_finding__do_update_description',
            'backend_api_resolvers_finding__do_update_evidence_description',
            'backend_api_resolvers_finding__do_update_severity',
            'backend_api_resolvers_finding__get_analyst',
            'backend_api_resolvers_finding__get_historic_state',
            'backend_api_resolvers_finding__get_observations',
            'backend_api_resolvers_finding__get_pending_vulns',
            'backend_api_resolvers_finding_resolve_finding',
            'backend_api_resolvers_forces_resolve_forces_executions',
            'backend_api_resolvers_project__do_add_project_comment',
            'backend_api_resolvers_project__get_comments',
            'backend_api_resolvers_project__get_drafts',
            'backend_api_resolvers_project__get_events',
            'backend_api_resolvers_project__get_service_attributes',
            'backend_api_resolvers_project_resolve_project',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_resource_resolve_resources',
            'backend_api_resolvers_vulnerability__do_approve_vulnerability',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_upload_file',
            ('backend_api_resolvers_vulnerability_resolve_'
                'vulnerability_resolve_analyst'),
            ('backend_api_resolvers_vulnerability_resolve_'
                'vulnerability_resolve_last_analyst'),
        },
        tags={
            'drills',
        }
    )
)


ORGANIZATION_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    customer=dict(
        actions={
            ''
        },
        tags=set()
    ),
    customeradmin=dict(
        action={
            'grant_organization_level_role:customer',
            'grant_organization_level_role:customeradmin'
        },
        tags=set()
    )
)


# Map(role_name -> Map(actions|tags -> definition))
USER_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            'backend_api_resolvers_cache_resolve_invalidate_cache',
            'backend_api_resolvers_internal_project_resolve_project_name',
            'backend_api_resolvers_me__get_tags',
            'backend_api_resolvers_project__do_create_project',
            'backend_api_resolvers_project_resolve_alive_projects',
            'backend_api_resolvers_tag_resolve_tag',
            'backend_api_resolvers_user__do_add_user',
            'backend_api_resolvers_user_resolve_user_list_projects',
            'grant_user_level_role:admin',
            'grant_user_level_role:customer',
            'grant_user_level_role:internal_manager',
        },
        tags=set(),
    ),
    analyst=dict(
        actions={
            'backend_api_resolvers_internal_project_resolve_project_name',
            'backend_api_resolvers_cache_resolve_invalidate_cache',
            'backend_api_resolvers_project__do_create_project',
        },
        tags={
            'drills',
        },
    ),
    customer=dict(
        actions={
            'backend_api_resolvers_internal_project_resolve_project_name',
            'backend_api_resolvers_project__do_create_project',
        },
        tags=set(),
    ),
    internal_manager=dict(
        actions={
            'backend_api_resolvers_internal_project_resolve_project_name',
            'backend_api_resolvers_me__get_tags',
            'backend_api_resolvers_project__do_create_project',
            'backend_api_resolvers_tag_resolve_tag',
            'backend_api_resolvers_user_resolve_user_list_projects',
        },
        tags={
            'drills',
        },
    )
)


# Map(service -> feature)
SERVICE_ATTRIBUTES: Dict[str, Set[str]] = dict(
    drills_black={
        'has_drills_black',
        'is_fluidattacks_customer',
        'must_only_have_fluidattacks_hackers',
    },
    drills_white={
        'has_drills_white',
        'is_fluidattacks_customer',
        'must_only_have_fluidattacks_hackers',
    },
    forces={
        'has_forces',
        'is_fluidattacks_customer',
        'must_only_have_fluidattacks_hackers',
    },
    integrates={
        'has_integrates',
    },
)
