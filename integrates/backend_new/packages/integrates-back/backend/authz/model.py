# Standard library
from typing import (
    Dict,
    Set,
)


# Map(role_name -> Map(actions|tags -> definition))
GROUP_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_confirm_zero_risk_vuln_mutate',
            'backend_api_mutations_create_event_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_execute_skims_mutate',
            'backend_api_mutations_reject_zero_risk_vuln_mutate',
            'backend_api_mutations_request_zero_risk_vuln_mutate',
            'backend_api_mutations_remove_event_evidence_mutate',
            'backend_api_mutations_remove_group_mutate',
            'backend_api_mutations_solve_event_mutate',
            'backend_api_mutations_update_event_evidence_mutate',
            'backend_api_resolvers_new_query_event_resolve',
            'backend_api_resolvers_new_query_events_resolve',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_mutations_approve_draft_mutate',
            'backend_api_mutations_create_draft_mutate',
            'backend_api_mutations_delete_finding_mutate',
            'backend_api_resolvers_finding__do_reject_draft',
            'backend_api_resolvers_finding__do_remove_evidence',
            'backend_api_mutations_submit_draft_mutate',
            'backend_api_resolvers_finding__do_update_description',
            'backend_api_mutations_update_evidence_description_mutate',
            'backend_api_mutations_update_evidence_mutate',
            'backend_api_mutations_update_severity_mutate',
            'backend_api_resolvers_new_finding_sorts_resolve',
            'backend_api_resolvers_new_finding_analyst_resolve',
            'backend_api_resolvers_new_finding_historic_state_resolve',
            'backend_api_resolvers_new_finding_observations_resolve',
            'backend_api_resolvers_new_query_finding_resolve',
            'backend_api_resolvers_new_query_finding__get_draft',
            (
                'backend_api_resolvers_new_vulnerability_'
                'historic_verification_resolve'
            ),
            (
                'backend_api_resolvers_new_vulnerability_'
                'historic_zero_risk_resolve'
            ),
            'backend_api_resolvers_new_query_vulnerability_resolve',
            'backend_api_resolvers_new_query_forces_executions_resolve',
            'backend_api_resolvers_new_query_forces_executions_new_resolve',
            'backend_api_resolvers_new_query_forces_execution_resolve',
            'backend_api_resolvers_organization__do_move_group_organization',
            'backend_api_resolvers_project__do_add_project_consult',
            'backend_api_resolvers_project__do_add_tags',
            'backend_api_resolvers_project__do_edit_group',
            'backend_api_resolvers_project__do_reject_remove_project',
            'backend_api_resolvers_project__do_remove_tag',
            'backend_api_resolvers_new_group_analytics_resolve',
            'backend_api_resolvers_new_group_bill_resolve',
            'backend_api_resolvers_new_group_consulting_resolve',
            'backend_api_resolvers_new_group_drafts_resolve',
            'backend_api_resolvers_new_group_events_resolve',
            'backend_api_resolvers_new_group_service_attributes_resolve',
            'backend_api_resolvers_new_group_stakeholders_resolve',
            'backend_api_resolvers_new_query_group_resolve',
            'backend_api_resolvers_new_query_report__get_url_group_report',
            'backend_api_resolvers_resource__do_add_environments',
            'backend_api_resolvers_resource__do_add_files',
            'backend_api_resolvers_resource__do_add_repositories',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_add_ip_root_mutate',
            'backend_api_mutations_add_url_root_mutate',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_resource__do_remove_files',
            'backend_api_resolvers_resource__do_update_environment',
            'backend_api_resolvers_resource__do_update_repository',
            'backend_api_resolvers_resource_resolve_add_resources',
            'backend_api_resolvers_new_query_resources_resolve',
            'backend_api_resolvers_user__do_edit_stakeholder',
            'backend_api_resolvers_user__do_grant_stakeholder_access',
            'backend_api_resolvers_user__do_remove_stakeholder_access',
            'backend_api_mutations_update_forces_access_token_mutate',
            'backend_api_resolvers_new_query_stakeholder__resolve_for_group',
            'backend_api_mutations_delete_vulnerability_mutate',
            'backend_api_resolvers_vulnerability__do_download_vuln_file',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_mutations_upload_file_mutate',
            'backend_api_resolvers_vulnerability__do_verify_request_vuln',
            'backend_api_resolvers_new_vulnerability_analyst_resolve',
            'grant_group_level_role:analyst',
            'grant_group_level_role:closer',
            'grant_group_level_role:customer',
            'grant_group_level_role:customeradmin',
            'grant_group_level_role:executive',
            'grant_group_level_role:group_manager',
            'grant_group_level_role:resourcer',
            'grant_group_level_role:reviewer',
            'post_finding_observation'
        },
        tags=set(),
    ),
    analyst=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_create_event_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_remove_event_evidence_mutate',
            'backend_api_mutations_solve_event_mutate',
            'backend_api_mutations_update_event_evidence_mutate',
            'backend_api_resolvers_new_query_event_resolve',
            'backend_api_resolvers_new_query_events_resolve',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_mutations_create_draft_mutate',
            'backend_api_mutations_delete_finding_mutate',
            'backend_api_resolvers_finding__do_reject_draft',
            'backend_api_resolvers_finding__do_remove_evidence',
            'backend_api_mutations_submit_draft_mutate',
            'backend_api_resolvers_finding__do_update_description',
            'backend_api_mutations_update_evidence_description_mutate',
            'backend_api_mutations_update_evidence_mutate',
            'backend_api_mutations_update_severity_mutate',
            'backend_api_resolvers_new_finding_analyst_resolve',
            'backend_api_resolvers_new_finding_historic_state_resolve',
            'backend_api_resolvers_new_finding_observations_resolve',
            'backend_api_resolvers_new_query_finding_resolve',
            'backend_api_resolvers_new_query_finding__get_draft',
            'backend_api_resolvers_new_finding_sorts_resolve',
            (
                'backend_api_resolvers_new_vulnerability_'
                'historic_verification_resolve'
            ),
            'backend_api_resolvers_new_query_vulnerability_resolve',
            'backend_api_resolvers_new_query_forces_executions_resolve',
            'backend_api_resolvers_new_query_forces_executions_new_resolve',
            'backend_api_resolvers_new_query_forces_execution_resolve',
            'backend_api_resolvers_project__do_add_project_consult',
            'backend_api_resolvers_new_group_analytics_resolve',
            'backend_api_resolvers_new_group_consulting_resolve',
            'backend_api_resolvers_new_group_drafts_resolve',
            'backend_api_resolvers_new_group_events_resolve',
            'backend_api_resolvers_new_group_service_attributes_resolve',
            'backend_api_resolvers_new_query_group_resolve',
            'backend_api_resolvers_new_query_report__get_url_group_report',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_new_query_resources_resolve',
            'backend_api_mutations_delete_vulnerability_mutate',
            'backend_api_resolvers_vulnerability__do_download_vuln_file',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_mutations_upload_file_mutate',
            'backend_api_resolvers_vulnerability__do_verify_request_vuln',
            'backend_api_resolvers_new_vulnerability_analyst_resolve',
            'post_finding_observation'
        },
        tags={
            'drills',
        },
    ),
    closer=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_execute_skims_mutate',
            'backend_api_mutations_create_event_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_solve_event_mutate',
            'backend_api_resolvers_new_query_event_resolve',
            'backend_api_resolvers_new_query_events_resolve',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_finding__do_remove_evidence',
            'backend_api_resolvers_finding__do_update_description',
            'backend_api_mutations_update_evidence_description_mutate',
            'backend_api_mutations_update_evidence_mutate',
            'backend_api_resolvers_new_finding_analyst_resolve',
            'backend_api_resolvers_new_finding_historic_state_resolve',
            'backend_api_resolvers_new_query_finding_resolve',
            (
                'backend_api_resolvers_new_vulnerability_'
                'historic_verification_resolve'
            ),
            'backend_api_resolvers_new_query_vulnerability_resolve',
            'backend_api_resolvers_new_query_forces_executions_resolve',
            'backend_api_resolvers_new_query_forces_executions_new_resolve',
            'backend_api_resolvers_new_query_forces_execution_resolve',
            'backend_api_resolvers_new_group_analytics_resolve',
            'backend_api_resolvers_new_group_consulting_resolve',
            'backend_api_resolvers_new_group_events_resolve',
            'backend_api_resolvers_new_group_service_attributes_resolve',
            'backend_api_resolvers_new_query_group_resolve',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_new_query_resources_resolve',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_download_vuln_file',
            'backend_api_mutations_upload_file_mutate',
            'backend_api_resolvers_vulnerability__do_verify_request_vuln',
            'backend_api_resolvers_new_vulnerability_analyst_resolve',
        },
        tags={
            'drills',
        },
    ),
    customer=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_request_zero_risk_vuln_mutate',
            'backend_api_mutations_update_vulns_treatment_mutate',
            'backend_api_resolvers_new_query_event_resolve',
            'backend_api_resolvers_new_query_events_resolve',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_finding__do_update_client_description',
            'backend_api_resolvers_new_query_finding_resolve',
            (
                'backend_api_resolvers_new_vulnerability_'
                'historic_zero_risk_resolve'
            ),
            'backend_api_resolvers_new_query_vulnerability_resolve',
            'backend_api_resolvers_new_query_forces_executions_resolve',
            'backend_api_resolvers_new_query_forces_executions_new_resolve',
            'backend_api_resolvers_new_query_forces_execution_resolve',
            'backend_api_resolvers_project__do_add_project_consult',
            'backend_api_resolvers_project__do_add_tags',
            'backend_api_resolvers_project__do_remove_tag',
            'backend_api_resolvers_new_group_analytics_resolve',
            'backend_api_resolvers_new_group_bill_resolve',
            'backend_api_resolvers_new_group_consulting_resolve',
            'backend_api_resolvers_new_group_events_resolve',
            'backend_api_resolvers_new_group_service_attributes_resolve',
            'backend_api_resolvers_new_query_group_resolve',
            'backend_api_resolvers_resource__do_add_environments',
            'backend_api_resolvers_resource__do_add_files',
            'backend_api_resolvers_resource__do_add_repositories',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_add_ip_root_mutate',
            'backend_api_mutations_add_url_root_mutate',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_resource__do_remove_files',
            'backend_api_resolvers_resource__do_update_environment',
            'backend_api_resolvers_resource__do_update_repository',
            'backend_api_resolvers_resource_resolve_add_resources',
            'backend_api_resolvers_new_query_resources_resolve',
            'backend_api_resolvers_vulnerability__do_delete_tags',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
            'valid_treatment_manager',
        },
        tags=set(),
    ),
    customeradmin=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_request_zero_risk_vuln_mutate',
            'backend_api_mutations_handle_vulns_acceptation_mutate',
            'backend_api_mutations_remove_group_mutate',
            'backend_api_mutations_update_vulns_treatment_mutate',
            'backend_api_resolvers_new_query_event_resolve',
            'backend_api_resolvers_new_query_events_resolve',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_finding__do_handle_acceptation',
            'backend_api_resolvers_finding__do_update_client_description',
            'backend_api_resolvers_new_query_finding_resolve',
            (
                'backend_api_resolvers_new_vulnerability_'
                'historic_zero_risk_resolve'
            ),
            'backend_api_resolvers_new_query_vulnerability_resolve',
            'backend_api_resolvers_new_query_forces_executions_resolve',
            'backend_api_resolvers_new_query_forces_executions_new_resolve',
            'backend_api_resolvers_new_query_forces_execution_resolve',
            'backend_api_resolvers_organization__do_move_group_organization',
            'backend_api_resolvers_project__do_add_project_consult',
            'backend_api_resolvers_project__do_add_tags',
            'backend_api_resolvers_project__do_edit_group',
            'backend_api_resolvers_project__do_reject_remove_project',
            'backend_api_resolvers_project__do_remove_tag',
            'backend_api_resolvers_new_group_analytics_resolve',
            'backend_api_resolvers_new_group_bill_resolve',
            'backend_api_resolvers_new_group_consulting_resolve',
            'backend_api_resolvers_new_group_events_resolve',
            'backend_api_resolvers_new_group_service_attributes_resolve',
            'backend_api_resolvers_new_group_stakeholders_resolve',
            'backend_api_resolvers_new_query_group_resolve',
            'backend_api_resolvers_new_query_report__get_url_group_report',
            'backend_api_resolvers_resource__do_add_environments',
            'backend_api_resolvers_resource__do_add_files',
            'backend_api_resolvers_resource__do_add_repositories',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_add_ip_root_mutate',
            'backend_api_mutations_add_url_root_mutate',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_resource__do_remove_files',
            'backend_api_resolvers_resource__do_update_environment',
            'backend_api_resolvers_resource__do_update_repository',
            'backend_api_resolvers_resource_resolve_add_resources',
            'backend_api_resolvers_new_query_resources_resolve',
            'backend_api_resolvers_user__do_edit_stakeholder',
            'backend_api_resolvers_user__do_grant_stakeholder_access',
            'backend_api_resolvers_user__do_remove_stakeholder_access',
            'backend_api_resolvers_new_query_stakeholder__resolve_for_group',
            'backend_api_resolvers_vulnerability__do_delete_tags',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
            'grant_user_level_role:customer',
            'grant_group_level_role:customer',
            'grant_group_level_role:customeradmin',
            'grant_group_level_role:executive',
            'valid_treatment_manager',
        },
        tags=set(),
    ),
    executive=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_update_vulns_treatment_mutate',
            'backend_api_resolvers_new_query_event_resolve',
            'backend_api_resolvers_new_query_events_resolve',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_finding__do_update_client_description',
            'backend_api_resolvers_new_query_finding_resolve',
            'backend_api_resolvers_new_query_vulnerability_resolve',
            'backend_api_resolvers_new_query_forces_executions_resolve',
            'backend_api_resolvers_new_query_forces_executions_new_resolve',
            'backend_api_resolvers_new_query_forces_execution_resolve',
            'backend_api_resolvers_project__do_add_project_consult',
            'backend_api_resolvers_project__do_add_tags',
            'backend_api_resolvers_project__do_remove_tag',
            'backend_api_resolvers_new_group_analytics_resolve',
            'backend_api_resolvers_new_group_consulting_resolve',
            'backend_api_resolvers_new_group_events_resolve',
            'backend_api_resolvers_new_group_service_attributes_resolve',
            'backend_api_resolvers_new_query_group_resolve',
            'backend_api_resolvers_resource__do_add_environments',
            'backend_api_resolvers_resource__do_add_files',
            'backend_api_resolvers_resource__do_add_repositories',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_add_ip_root_mutate',
            'backend_api_mutations_add_url_root_mutate',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_resource__do_remove_files',
            'backend_api_resolvers_resource__do_update_environment',
            'backend_api_resolvers_resource__do_update_repository',
            'backend_api_resolvers_resource_resolve_add_resources',
            'backend_api_resolvers_new_query_resources_resolve',
            'backend_api_resolvers_vulnerability__do_delete_tags',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
        },
        tags=set()
    ),
    group_manager=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_create_event_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_solve_event_mutate',
            'backend_api_mutations_handle_vulns_acceptation_mutate',
            'backend_api_mutations_remove_group_mutate',
            'backend_api_mutations_update_vulns_treatment_mutate',
            'backend_api_resolvers_new_query_event_resolve',
            'backend_api_resolvers_new_query_events_resolve',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_finding__do_handle_acceptation',
            'backend_api_resolvers_finding__do_update_client_description',
            'backend_api_resolvers_new_finding_analyst_resolve',
            'backend_api_resolvers_new_finding_observations_resolve',
            'backend_api_resolvers_new_query_finding_resolve',
            'backend_api_resolvers_new_query_finding__get_draft',
            'backend_api_resolvers_new_query_vulnerability_resolve',
            'backend_api_resolvers_new_query_forces_executions_resolve',
            'backend_api_resolvers_new_query_forces_executions_new_resolve',
            'backend_api_resolvers_new_query_forces_execution_resolve',
            'backend_api_resolvers_organization__do_move_group_organization',
            'backend_api_resolvers_project__do_add_project_consult',
            'backend_api_resolvers_project__do_add_tags',
            'backend_api_resolvers_project__do_edit_group',
            'backend_api_resolvers_project__do_reject_remove_project',
            'backend_api_resolvers_project__do_remove_tag',
            'backend_api_resolvers_new_group_analytics_resolve',
            'backend_api_resolvers_new_group_bill_resolve',
            'backend_api_resolvers_new_group_consulting_resolve',
            'backend_api_resolvers_new_group_drafts_resolve',
            'backend_api_resolvers_new_group_events_resolve',
            'backend_api_resolvers_new_group_service_attributes_resolve',
            'backend_api_resolvers_new_group_stakeholders_resolve',
            'backend_api_resolvers_new_query_group_resolve',
            'backend_api_resolvers_new_query_report__get_url_group_report',
            'backend_api_resolvers_resource__do_add_environments',
            'backend_api_resolvers_resource__do_add_files',
            'backend_api_resolvers_resource__do_add_repositories',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_add_ip_root_mutate',
            'backend_api_mutations_add_url_root_mutate',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_resource__do_remove_files',
            'backend_api_resolvers_resource__do_update_environment',
            'backend_api_resolvers_resource__do_update_repository',
            'backend_api_resolvers_resource_resolve_add_resources',
            'backend_api_resolvers_new_query_resources_resolve',
            'backend_api_resolvers_user__do_edit_stakeholder',
            'backend_api_resolvers_user__do_grant_stakeholder_access',
            'backend_api_resolvers_user__do_remove_stakeholder_access',
            'backend_api_mutations_update_forces_access_token_mutate',
            'backend_api_resolvers_new_query_stakeholder__resolve_for_group',
            'backend_api_resolvers_vulnerability__do_delete_tags',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
            'backend_api_resolvers_new_vulnerability_analyst_resolve',
            'grant_group_level_role:analyst',
            'grant_group_level_role:closer',
            'grant_user_level_role:customer',
            'grant_group_level_role:customer',
            'grant_group_level_role:customeradmin',
            'grant_group_level_role:executive',
            'grant_group_level_role:group_manager',
            'grant_group_level_role:reviewer',
            'grant_group_level_role:resourcer',
            'post_finding_observation',
            'valid_treatment_manager',
        },
        tags=set(),
    ),
    resourcer=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_create_event_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_resolvers_new_query_event_resolve',
            'backend_api_resolvers_new_query_events_resolve',
            'backend_api_mutations_solve_event_mutate',
            'backend_api_resolvers_new_query_finding_resolve',
            'backend_api_resolvers_new_query_vulnerability_resolve',
            'backend_api_resolvers_new_query_forces_executions_resolve',
            'backend_api_resolvers_new_query_forces_executions_new_resolve',
            'backend_api_resolvers_new_query_forces_execution_resolve',
            'backend_api_resolvers_new_group_analytics_resolve',
            'backend_api_resolvers_new_group_consulting_resolve',
            'backend_api_resolvers_new_group_events_resolve',
            'backend_api_resolvers_new_group_service_attributes_resolve',
            'backend_api_resolvers_new_query_group_resolve',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_new_query_resources_resolve',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
        },
        tags={
            'drills',
        },
    ),
    reviewer=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_confirm_zero_risk_vuln_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_reject_zero_risk_vuln_mutate',
            'backend_api_resolvers_new_query_event_resolve',
            'backend_api_resolvers_new_query_events_resolve',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_mutations_approve_draft_mutate',
            'backend_api_mutations_delete_finding_mutate',
            'backend_api_resolvers_finding__do_reject_draft',
            'backend_api_resolvers_finding__do_update_description',
            'backend_api_mutations_update_evidence_description_mutate',
            'backend_api_mutations_update_severity_mutate',
            'backend_api_resolvers_new_finding_analyst_resolve',
            'backend_api_resolvers_new_finding_historic_state_resolve',
            'backend_api_resolvers_new_finding_observations_resolve',
            'backend_api_resolvers_new_query_finding_resolve',
            'backend_api_resolvers_new_query_finding__get_draft',
            (
                'backend_api_resolvers_new_vulnerability_'
                'historic_verification_resolve'
            ),
            (
                'backend_api_resolvers_new_vulnerability_'
                'historic_zero_risk_resolve'
            ),
            'backend_api_resolvers_new_query_vulnerability_resolve',
            'backend_api_resolvers_new_query_forces_executions_resolve',
            'backend_api_resolvers_new_query_forces_executions_new_resolve',
            'backend_api_resolvers_new_query_forces_execution_resolve',
            'backend_api_resolvers_project__do_add_project_consult',
            'backend_api_resolvers_new_group_analytics_resolve',
            'backend_api_resolvers_new_group_consulting_resolve',
            'backend_api_resolvers_new_group_drafts_resolve',
            'backend_api_resolvers_new_group_events_resolve',
            'backend_api_resolvers_new_group_service_attributes_resolve',
            'backend_api_resolvers_new_group_stakeholders_resolve',
            'backend_api_resolvers_new_query_group_resolve',
            'backend_api_resolvers_resource__do_download_file',
            'backend_api_resolvers_new_query_resources_resolve',
            'backend_api_resolvers_new_query_stakeholder__resolve_for_group',
            ('backend_api_resolvers_vulnerability__do_'
                'request_verification_vuln'),
            'backend_api_mutations_upload_file_mutate',
            'backend_api_resolvers_new_vulnerability_analyst_resolve',
            'post_finding_observation'
        },
        tags={
            'drills',
        }
    ),
    service_forces=dict(
        actions={
            'backend_api_mutations_add_forces_execution_mutate',
            'backend_api_resolvers_new_query_group_resolve',
            'backend_api_resolvers_new_query_finding_resolve',
            'backend_api_resolvers_new_query_vulnerability_resolve',
        },
        tags={
            'forces'
        }
    ),
)

GROUP_LEVEL_ACTIONS: Set[str] = {
    action
    for definition in GROUP_LEVEL_ROLES.values()
    for action in definition['actions']
}

ORGANIZATION_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            'backend_api_mutations_edit_stakeholder_organization_mutate',
            (
                'backend_api_mutations_grant_stakeholder_organization_access'
                '_mutate'
            ),
            (
                'backend_api_mutations_remove_stakeholder_organization_access'
                '_mutate'
            ),
            'backend_api_mutations_update_organization_policies_mutate',
            'backend_api_resolvers_new_organization_analytics_resolve',
            'backend_api_resolvers_new_organization_stakeholders_resolve',
            (
                'backend_api_resolvers_new_query_stakeholder_'
                '_resolve_for_organization'
            ),
            'backend_api_resolvers_project__do_create_project',
            'grant_organization_level_role:customer',
            'grant_organization_level_role:customeradmin'
        },
        tags=set()
    ),
    customer=dict(
        actions={
            'backend_api_resolvers_new_organization_analytics_resolve',
            'backend_api_resolvers_project__do_create_project',
        },
        tags=set()
    ),
    customeradmin=dict(
        actions={
            'backend_api_mutations_edit_stakeholder_organization_mutate',
            (
                'backend_api_mutations_grant_stakeholder_organization_access'
                '_mutate'
            ),
            (
                'backend_api_mutations_remove_stakeholder_organization_access'
                '_mutate'
            ),
            'backend_api_mutations_update_organization_policies_mutate',
            'backend_api_resolvers_new_organization_analytics_resolve',
            'backend_api_resolvers_new_organization_stakeholders_resolve',
            (
                'backend_api_resolvers_new_query_stakeholder_'
                '_resolve_for_organization'
            ),
            'backend_api_resolvers_project__do_create_project',
            'grant_organization_level_role:customer',
            'grant_organization_level_role:customeradmin'
        },
        tags=set()
    ),
    group_manager=dict(
        actions={
            'backend_api_mutations_edit_stakeholder_organization_mutate',
            (
                'backend_api_mutations_grant_stakeholder_organization_access'
                '_mutate'
            ),
            (
                'backend_api_mutations_remove_stakeholder_organization_access'
                '_mutate'
            ),
            'backend_api_resolvers_new_organization_analytics_resolve',
            'backend_api_resolvers_new_organization_stakeholders_resolve',
            (
                'backend_api_resolvers_new_query_stakeholder_'
                '_resolve_for_organization'
            ),
            'backend_api_resolvers_project__do_create_project',
        },
        tags=set()
    )
)

ORGANIZATION_LEVEL_ACTIONS: Set[str] = {
    action
    for definition in ORGANIZATION_LEVEL_ROLES.values()
    for action in definition['actions']
}

# Map(role_name -> Map(actions|tags -> definition))
USER_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            'backend_api_mutations_invalidate_cache_mutate',
            'backend_api_resolvers_new_query_internal_names_resolve',
            'backend_api_resolvers_project__do_create_project',
            'backend_api_resolvers_new_query_groups_resolve',
            'backend_api_resolvers_new_query_report__get_url_all_users',
            'backend_api_resolvers_new_query_report__get_url_all_vulns',
            'backend_api_mutations_add_stakeholder_mutate',
            'backend_api_resolvers_new_query_user_list_groups_resolve',
            'grant_user_level_role:admin',
            'grant_user_level_role:customer',
            'grant_user_level_role:internal_manager',
        },
        tags=set(),
    ),
    analyst=dict(
        actions={
            'backend_api_resolvers_new_query_internal_names_resolve',
            'backend_api_mutations_invalidate_cache_mutate',
            'backend_api_resolvers_project__do_create_project',
        },
        tags={
            'drills',
        },
    ),
    customer=dict(
        actions={
            'backend_api_resolvers_new_query_internal_names_resolve',
            'backend_api_resolvers_project__do_create_project',
        },
        tags=set(),
    ),
    internal_manager=dict(
        actions={
            'backend_api_resolvers_new_query_internal_names_resolve',
            'backend_api_resolvers_project__do_create_project',
            'backend_api_resolvers_new_query_user_list_groups_resolve',
        },
        tags={
            'drills',
        },
    )
)

USER_LEVEL_ACTIONS: Set[str] = {
    action
    for definition in USER_LEVEL_ROLES.values()
    for action in definition['actions']
}

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

SERVICE_ATTRIBUTES_SET: Set[str] = {
    action
    for actions in SERVICE_ATTRIBUTES.values()
    for action in actions
}
