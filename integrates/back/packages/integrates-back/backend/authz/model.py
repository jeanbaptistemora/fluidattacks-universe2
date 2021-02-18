# Standard library
from typing import (
    Dict,
    Set,
)

# Constants
FLUID_IDENTIFIER = '@fluidattacks.com'

# Map(role_name -> Map(actions|tags -> definition))
GROUP_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_add_files_mutate',
            'backend_api_mutations_add_finding_consult_mutate',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_add_group_consult_mutate',
            'backend_api_mutations_add_group_tags_mutate',
            'backend_api_mutations_add_ip_root_mutate',
            'backend_api_mutations_add_url_root_mutate',
            'backend_api_mutations_approve_draft_mutate',
            'backend_api_mutations_confirm_zero_risk_vuln_mutate',
            'backend_api_mutations_create_draft_mutate',
            'backend_api_mutations_create_event_mutate',
            'backend_api_mutations_delete_finding_mutate',
            'backend_api_mutations_delete_vulnerability_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_download_file_mutate',
            'backend_api_mutations_download_vulnerability_file_mutate',
            'backend_api_mutations_edit_group_mutate',
            'backend_api_mutations_edit_stakeholder_mutate',
            'backend_api_mutations_grant_stakeholder_access_mutate',
            'backend_api_mutations_reject_draft_mutate',
            'backend_api_mutations_reject_zero_risk_vuln_mutate',
            'backend_api_mutations_remove_event_evidence_mutate',
            'backend_api_mutations_remove_files_mutate',
            'backend_api_mutations_remove_finding_evidence_mutate',
            'backend_api_mutations_remove_group_mutate',
            'backend_api_mutations_remove_group_tag_mutate',
            'backend_api_mutations_remove_stakeholder_access_mutate',
            'backend_api_mutations_request_verification_vulnerability_mutate',
            'backend_api_mutations_request_zero_risk_vuln_mutate',
            'backend_api_mutations_solve_event_mutate',
            'backend_api_mutations_submit_draft_mutate',
            'backend_api_mutations_unsubscribe_from_group_mutate',
            'backend_api_mutations_update_event_evidence_mutate',
            'backend_api_mutations_update_evidence_description_mutate',
            'backend_api_mutations_update_evidence_mutate',
            'backend_api_mutations_update_finding_description_mutate',
            'backend_api_mutations_update_forces_access_token_mutate',
            'backend_api_mutations_update_git_environments_mutate',
            'backend_api_mutations_update_git_root_mutate',
            'backend_api_mutations_update_root_cloning_status_mutate',
            'backend_api_mutations_update_root_state_mutate',
            'backend_api_mutations_update_severity_mutate',
            'backend_api_mutations_upload_file_mutate',
            'backend_api_mutations_verify_request_vulnerability_mutate',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_finding_analyst_resolve',
            'backend_api_resolvers_finding_historic_state_resolve',
            'backend_api_resolvers_finding_observations_resolve',
            'backend_api_resolvers_finding_sorts_resolve',
            'backend_api_resolvers_finding_zero_risk_resolve',
            'backend_api_resolvers_group_analytics_resolve',
            'backend_api_resolvers_group_bill_resolve',
            'backend_api_resolvers_group_consulting_resolve',
            'backend_api_resolvers_group_drafts_resolve',
            'backend_api_resolvers_group_forces_token_resolve',
            'backend_api_resolvers_group_events_resolve',
            'backend_api_resolvers_group_service_attributes_resolve',
            'backend_api_resolvers_group_stakeholders_resolve',
            'backend_api_resolvers_organization__do_move_group_organization',
            'backend_api_resolvers_query_event_resolve',
            'backend_api_resolvers_query_events_resolve',
            'backend_api_resolvers_query_finding__get_draft',
            'backend_api_resolvers_query_finding_resolve',
            'backend_api_resolvers_query_forces_execution_resolve',
            'backend_api_resolvers_query_forces_executions_new_resolve',
            'backend_api_resolvers_query_forces_executions_resolve',
            'backend_api_resolvers_query_group_resolve',
            'backend_api_resolvers_query_report__get_url_group_report',
            'backend_api_resolvers_query_resources_resolve',
            'backend_api_resolvers_query_stakeholder__resolve_for_group',
            'backend_api_resolvers_query_vulnerability_resolve',
            'backend_api_resolvers_vulnerability_analyst_resolve',
            (
                'backend_api_resolvers_vulnerability_'
                'historic_verification_resolve'
            ),
            (
                'backend_api_resolvers_vulnerability_'
                'historic_zero_risk_resolve'
            ),
            'grant_group_level_role:analyst',
            'grant_group_level_role:closer',
            'grant_group_level_role:customer',
            'grant_group_level_role:customeradmin',
            'grant_group_level_role:executive',
            'grant_group_level_role:group_manager',
            'grant_group_level_role:resourcer',
            'grant_group_level_role:reviewer',
            'post_finding_observation',
            'update_git_root_filter',
        },
        tags=set(),
    ),
    analyst=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_add_finding_consult_mutate',
            'backend_api_mutations_add_group_consult_mutate',
            'backend_api_mutations_create_draft_mutate',
            'backend_api_mutations_create_event_mutate',
            'backend_api_mutations_delete_finding_mutate',
            'backend_api_mutations_delete_vulnerability_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_download_file_mutate',
            'backend_api_mutations_download_vulnerability_file_mutate',
            'backend_api_mutations_reject_draft_mutate',
            'backend_api_mutations_remove_event_evidence_mutate',
            'backend_api_mutations_remove_finding_evidence_mutate',
            'backend_api_mutations_request_verification_vulnerability_mutate',
            'backend_api_mutations_solve_event_mutate',
            'backend_api_mutations_submit_draft_mutate',
            'backend_api_mutations_unsubscribe_from_group_mutate',
            'backend_api_mutations_update_event_evidence_mutate',
            'backend_api_mutations_update_evidence_description_mutate',
            'backend_api_mutations_update_evidence_mutate',
            'backend_api_mutations_update_finding_description_mutate',
            'backend_api_mutations_update_severity_mutate',
            'backend_api_mutations_upload_file_mutate',
            'backend_api_mutations_verify_request_vulnerability_mutate',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_finding_analyst_resolve',
            'backend_api_resolvers_finding_historic_state_resolve',
            'backend_api_resolvers_finding_observations_resolve',
            'backend_api_resolvers_finding_sorts_resolve',
            'backend_api_resolvers_group_analytics_resolve',
            'backend_api_resolvers_group_consulting_resolve',
            'backend_api_resolvers_group_drafts_resolve',
            'backend_api_resolvers_group_events_resolve',
            'backend_api_resolvers_group_service_attributes_resolve',
            'backend_api_resolvers_query_event_resolve',
            'backend_api_resolvers_query_events_resolve',
            'backend_api_resolvers_query_finding__get_draft',
            'backend_api_resolvers_query_finding_resolve',
            'backend_api_resolvers_query_forces_execution_resolve',
            'backend_api_resolvers_query_forces_executions_new_resolve',
            'backend_api_resolvers_query_forces_executions_resolve',
            'backend_api_resolvers_query_group_resolve',
            'backend_api_resolvers_query_report__get_url_group_report',
            'backend_api_resolvers_query_resources_resolve',
            'backend_api_resolvers_query_vulnerability_resolve',
            'backend_api_resolvers_vulnerability_analyst_resolve',
            (
                'backend_api_resolvers_vulnerability_'
                'historic_verification_resolve'
            ),
            'post_finding_observation',
        },
        tags={
            'drills',
        },
    ),
    closer=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_add_finding_consult_mutate',
            'backend_api_mutations_create_event_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_download_file_mutate',
            'backend_api_mutations_download_vulnerability_file_mutate',
            'backend_api_mutations_remove_finding_evidence_mutate',
            'backend_api_mutations_request_verification_vulnerability_mutate',
            'backend_api_mutations_solve_event_mutate',
            'backend_api_mutations_unsubscribe_from_group_mutate',
            'backend_api_mutations_update_evidence_description_mutate',
            'backend_api_mutations_update_evidence_mutate',
            'backend_api_mutations_update_finding_description_mutate',
            'backend_api_mutations_update_root_cloning_status_mutate',
            'backend_api_mutations_upload_file_mutate',
            'backend_api_mutations_verify_request_vulnerability_mutate',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_finding_analyst_resolve',
            'backend_api_resolvers_finding_historic_state_resolve',
            'backend_api_resolvers_group_analytics_resolve',
            'backend_api_resolvers_group_consulting_resolve',
            'backend_api_resolvers_group_events_resolve',
            'backend_api_resolvers_group_service_attributes_resolve',
            'backend_api_resolvers_query_event_resolve',
            'backend_api_resolvers_query_events_resolve',
            'backend_api_resolvers_query_finding_resolve',
            'backend_api_resolvers_query_forces_execution_resolve',
            'backend_api_resolvers_query_forces_executions_new_resolve',
            'backend_api_resolvers_query_forces_executions_resolve',
            'backend_api_resolvers_query_group_resolve',
            'backend_api_resolvers_query_resources_resolve',
            'backend_api_resolvers_query_vulnerability_resolve',
            'backend_api_resolvers_vulnerability_analyst_resolve',
            (
                'backend_api_resolvers_vulnerability_'
                'historic_verification_resolve'
            ),
        },
        tags={
            'drills',
        },
    ),
    customer=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_add_files_mutate',
            'backend_api_mutations_add_finding_consult_mutate',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_add_group_consult_mutate',
            'backend_api_mutations_add_group_tags_mutate',
            'backend_api_mutations_add_ip_root_mutate',
            'backend_api_mutations_add_url_root_mutate',
            'backend_api_mutations_delete_vulnerability_tags_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_download_file_mutate',
            'backend_api_mutations_remove_files_mutate',
            'backend_api_mutations_remove_group_tag_mutate',
            'backend_api_mutations_request_verification_vulnerability_mutate',
            'backend_api_mutations_request_zero_risk_vuln_mutate',
            'backend_api_mutations_unsubscribe_from_group_mutate',
            'backend_api_mutations_update_git_environments_mutate',
            'backend_api_mutations_update_git_root_mutate',
            'backend_api_mutations_update_root_state_mutate',
            'backend_api_mutations_update_treatment_vulnerability_mutate',
            'backend_api_mutations_update_vulns_treatment_mutate',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_group_analytics_resolve',
            'backend_api_resolvers_group_bill_resolve',
            'backend_api_resolvers_group_consulting_resolve',
            'backend_api_resolvers_group_events_resolve',
            'backend_api_resolvers_group_service_attributes_resolve',
            'backend_api_resolvers_query_event_resolve',
            'backend_api_resolvers_query_events_resolve',
            'backend_api_resolvers_query_finding_resolve',
            'backend_api_resolvers_query_forces_execution_resolve',
            'backend_api_resolvers_query_forces_executions_new_resolve',
            'backend_api_resolvers_query_forces_executions_resolve',
            'backend_api_resolvers_query_group_resolve',
            'backend_api_resolvers_query_resources_resolve',
            'backend_api_resolvers_query_vulnerability_resolve',
            'backend_api_resolvers_vulnerability_historic_zero_risk_resolve',
            'update_git_root_filter',
            'valid_treatment_manager',
        },
        tags=set(),
    ),
    customeradmin=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_add_files_mutate',
            'backend_api_mutations_add_finding_consult_mutate',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_add_group_consult_mutate',
            'backend_api_mutations_add_group_tags_mutate',
            'backend_api_mutations_add_ip_root_mutate',
            'backend_api_mutations_add_url_root_mutate',
            'backend_api_mutations_delete_vulnerability_tags_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_download_file_mutate',
            'backend_api_mutations_edit_group_mutate',
            'backend_api_mutations_edit_stakeholder_mutate',
            'backend_api_mutations_grant_stakeholder_access_mutate',
            'backend_api_mutations_handle_vulns_acceptation_mutate',
            'backend_api_mutations_remove_files_mutate',
            'backend_api_mutations_remove_group_mutate',
            'backend_api_mutations_remove_group_tag_mutate',
            'backend_api_mutations_remove_stakeholder_access_mutate',
            'backend_api_mutations_request_verification_vulnerability_mutate',
            'backend_api_mutations_request_zero_risk_vuln_mutate',
            'backend_api_mutations_unsubscribe_from_group_mutate',
            'backend_api_mutations_update_git_environments_mutate',
            'backend_api_mutations_update_git_root_mutate',
            'backend_api_mutations_update_root_state_mutate',
            'backend_api_mutations_update_treatment_vulnerability_mutate',
            'backend_api_mutations_update_vulns_treatment_mutate',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_group_analytics_resolve',
            'backend_api_resolvers_group_bill_resolve',
            'backend_api_resolvers_group_consulting_resolve',
            'backend_api_resolvers_group_events_resolve',
            'backend_api_resolvers_group_service_attributes_resolve',
            'backend_api_resolvers_group_stakeholders_resolve',
            'backend_api_resolvers_organization__do_move_group_organization',
            'backend_api_resolvers_query_event_resolve',
            'backend_api_resolvers_query_events_resolve',
            'backend_api_resolvers_query_finding_resolve',
            'backend_api_resolvers_query_forces_execution_resolve',
            'backend_api_resolvers_query_forces_executions_new_resolve',
            'backend_api_resolvers_query_forces_executions_resolve',
            'backend_api_resolvers_group_forces_token_resolve',
            'backend_api_resolvers_query_group_resolve',
            'backend_api_resolvers_query_report__get_url_group_report',
            'backend_api_resolvers_query_resources_resolve',
            'backend_api_resolvers_query_stakeholder__resolve_for_group',
            'backend_api_resolvers_query_vulnerability_resolve',
            'backend_api_resolvers_vulnerability_historic_zero_risk_resolve',
            'grant_group_level_role:customer',
            'grant_group_level_role:customeradmin',
            'grant_group_level_role:executive',
            'grant_user_level_role:customer',
            'update_git_root_filter',
            'valid_treatment_manager',
        },
        tags=set(),
    ),
    executive=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_add_files_mutate',
            'backend_api_mutations_add_finding_consult_mutate',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_add_group_consult_mutate',
            'backend_api_mutations_add_group_tags_mutate',
            'backend_api_mutations_add_ip_root_mutate',
            'backend_api_mutations_add_url_root_mutate',
            'backend_api_mutations_delete_vulnerability_tags_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_download_file_mutate',
            'backend_api_mutations_remove_files_mutate',
            'backend_api_mutations_remove_group_tag_mutate',
            'backend_api_mutations_request_verification_vulnerability_mutate',
            'backend_api_mutations_unsubscribe_from_group_mutate',
            'backend_api_mutations_update_git_environments_mutate',
            'backend_api_mutations_update_git_root_mutate',
            'backend_api_mutations_update_root_state_mutate',
            'backend_api_mutations_update_treatment_vulnerability_mutate',
            'backend_api_mutations_update_vulns_treatment_mutate',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_group_analytics_resolve',
            'backend_api_resolvers_group_consulting_resolve',
            'backend_api_resolvers_group_events_resolve',
            'backend_api_resolvers_group_service_attributes_resolve',
            'backend_api_resolvers_query_event_resolve',
            'backend_api_resolvers_query_events_resolve',
            'backend_api_resolvers_query_finding_resolve',
            'backend_api_resolvers_query_forces_execution_resolve',
            'backend_api_resolvers_query_forces_executions_new_resolve',
            'backend_api_resolvers_query_forces_executions_resolve',
            'backend_api_resolvers_query_group_resolve',
            'backend_api_resolvers_query_resources_resolve',
            'backend_api_resolvers_query_vulnerability_resolve',
        },
        tags=set()
    ),
    group_manager=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_add_files_mutate',
            'backend_api_mutations_add_finding_consult_mutate',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_add_group_consult_mutate',
            'backend_api_mutations_add_group_tags_mutate',
            'backend_api_mutations_add_ip_root_mutate',
            'backend_api_mutations_add_url_root_mutate',
            'backend_api_mutations_create_event_mutate',
            'backend_api_mutations_delete_vulnerability_tags_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_download_file_mutate',
            'backend_api_mutations_edit_group_mutate',
            'backend_api_mutations_edit_stakeholder_mutate',
            'backend_api_mutations_grant_stakeholder_access_mutate',
            'backend_api_mutations_handle_vulns_acceptation_mutate',
            'backend_api_mutations_remove_files_mutate',
            'backend_api_mutations_remove_group_mutate',
            'backend_api_mutations_remove_group_tag_mutate',
            'backend_api_mutations_remove_stakeholder_access_mutate',
            'backend_api_mutations_request_verification_vulnerability_mutate',
            'backend_api_mutations_request_zero_risk_vuln_mutate',
            'backend_api_mutations_solve_event_mutate',
            'backend_api_mutations_unsubscribe_from_group_mutate',
            'backend_api_mutations_update_forces_access_token_mutate',
            'backend_api_mutations_update_git_environments_mutate',
            'backend_api_mutations_update_git_root_mutate',
            'backend_api_mutations_update_root_state_mutate',
            'backend_api_mutations_update_treatment_vulnerability_mutate',
            'backend_api_mutations_update_vulns_treatment_mutate',
            'backend_api_mutations_update_forces_access_token_mutate',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_finding_analyst_resolve',
            'backend_api_resolvers_finding_observations_resolve',
            'backend_api_resolvers_group_analytics_resolve',
            'backend_api_resolvers_group_bill_resolve',
            'backend_api_resolvers_group_consulting_resolve',
            'backend_api_resolvers_group_drafts_resolve',
            'backend_api_resolvers_group_events_resolve',
            'backend_api_resolvers_group_service_attributes_resolve',
            'backend_api_resolvers_group_stakeholders_resolve',
            'backend_api_resolvers_organization__do_move_group_organization',
            'backend_api_resolvers_query_event_resolve',
            'backend_api_resolvers_query_events_resolve',
            'backend_api_resolvers_query_finding__get_draft',
            'backend_api_resolvers_query_finding_resolve',
            'backend_api_resolvers_query_forces_execution_resolve',
            'backend_api_resolvers_query_forces_executions_new_resolve',
            'backend_api_resolvers_query_forces_executions_resolve',
            'backend_api_resolvers_query_group_resolve',
            'backend_api_resolvers_query_report__get_url_group_report',
            'backend_api_resolvers_query_resources_resolve',
            'backend_api_resolvers_query_stakeholder__resolve_for_group',
            'backend_api_resolvers_query_vulnerability_resolve',
            'backend_api_resolvers_vulnerability_analyst_resolve',
            'backend_api_resolvers_vulnerability_historic_zero_risk_resolve',
            'grant_group_level_role:analyst',
            'grant_group_level_role:closer',
            'grant_group_level_role:customer',
            'grant_group_level_role:customeradmin',
            'grant_group_level_role:executive',
            'grant_group_level_role:group_manager',
            'grant_group_level_role:resourcer',
            'grant_group_level_role:reviewer',
            'grant_user_level_role:customer',
            'post_finding_observation',
            'update_git_root_filter',
            'valid_treatment_manager',
        },
        tags=set(),
    ),
    resourcer=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_add_git_root_mutate',
            'backend_api_mutations_create_event_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_download_file_mutate',
            'backend_api_mutations_request_verification_vulnerability_mutate',
            'backend_api_mutations_solve_event_mutate',
            'backend_api_mutations_unsubscribe_from_group_mutate',
            'backend_api_mutations_update_git_environments_mutate',
            'backend_api_mutations_update_git_root_mutate',
            'backend_api_mutations_update_root_cloning_status_mutate',
            'backend_api_resolvers_group_analytics_resolve',
            'backend_api_resolvers_group_consulting_resolve',
            'backend_api_resolvers_group_events_resolve',
            'backend_api_resolvers_group_service_attributes_resolve',
            'backend_api_resolvers_query_event_resolve',
            'backend_api_resolvers_query_events_resolve',
            'backend_api_resolvers_query_finding_resolve',
            'backend_api_resolvers_query_forces_execution_resolve',
            'backend_api_resolvers_query_forces_executions_new_resolve',
            'backend_api_resolvers_query_forces_executions_resolve',
            'backend_api_resolvers_query_group_resolve',
            'backend_api_resolvers_query_resources_resolve',
            'backend_api_resolvers_query_vulnerability_resolve',
            'update_git_root_filter',
        },
        tags={
            'drills',
        },
    ),
    reviewer=dict(
        actions={
            'backend_api_mutations_add_event_consult_mutate',
            'backend_api_mutations_add_finding_consult_mutate',
            'backend_api_mutations_add_group_consult_mutate',
            'backend_api_mutations_approve_draft_mutate',
            'backend_api_mutations_confirm_zero_risk_vuln_mutate',
            'backend_api_mutations_delete_finding_mutate',
            'backend_api_mutations_download_event_file_mutate',
            'backend_api_mutations_download_file_mutate',
            'backend_api_mutations_reject_draft_mutate',
            'backend_api_mutations_reject_zero_risk_vuln_mutate',
            'backend_api_mutations_request_verification_vulnerability_mutate',
            'backend_api_mutations_unsubscribe_from_group_mutate',
            'backend_api_mutations_update_evidence_description_mutate',
            'backend_api_mutations_update_finding_description_mutate',
            'backend_api_mutations_update_severity_mutate',
            'backend_api_mutations_upload_file_mutate',
            'backend_api_resolvers_finding__do_add_finding_consult',
            'backend_api_resolvers_finding_analyst_resolve',
            'backend_api_resolvers_finding_historic_state_resolve',
            'backend_api_resolvers_finding_observations_resolve',
            'backend_api_resolvers_finding_zero_risk_resolve',
            'backend_api_resolvers_group_analytics_resolve',
            'backend_api_resolvers_group_consulting_resolve',
            'backend_api_resolvers_group_drafts_resolve',
            'backend_api_resolvers_group_events_resolve',
            'backend_api_resolvers_group_service_attributes_resolve',
            'backend_api_resolvers_group_stakeholders_resolve',
            'backend_api_resolvers_query_event_resolve',
            'backend_api_resolvers_query_events_resolve',
            'backend_api_resolvers_query_finding__get_draft',
            'backend_api_resolvers_query_finding_resolve',
            'backend_api_resolvers_query_forces_execution_resolve',
            'backend_api_resolvers_query_forces_executions_new_resolve',
            'backend_api_resolvers_query_forces_executions_resolve',
            'backend_api_resolvers_query_group_resolve',
            'backend_api_resolvers_query_resources_resolve',
            'backend_api_resolvers_query_stakeholder__resolve_for_group',
            'backend_api_resolvers_query_vulnerability_resolve',
            'backend_api_resolvers_vulnerability_analyst_resolve',
            (
                'backend_api_resolvers_vulnerability_'
                'historic_verification_resolve'
            ),
            'backend_api_resolvers_vulnerability_historic_zero_risk_resolve',
            'handle_comment_scope',
            'post_finding_observation',
            'see_dropdown_to_confirm_zero_risk',
            'see_dropdown_to_reject_zero_risk',
        },
        tags={
            'drills',
        }
    ),
    service_forces=dict(
        actions={
            'backend_api_mutations_add_forces_execution_mutate',
            'backend_api_resolvers_query_finding_resolve',
            'backend_api_resolvers_query_group_resolve',
            'backend_api_resolvers_query_vulnerability_resolve',
            'backend_api_resolvers_vulnerability_historic_zero_risk_resolve',
        },
        tags={
            'forces'
        }
    ),
)

# Map(role_name -> Map(actions|tags -> definition))
GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS: Dict[str, Dict[str, Set[str]]] = dict(
    **GROUP_LEVEL_ROLES
)

GROUP_LEVEL_ACTIONS: Set[str] = {
    action
    for definition in GROUP_LEVEL_ROLES.values()
    for action in definition['actions']
}

GROUP_LEVEL_ACTIONS_FOR_FLUIDATTACKS: Set[str] = {
    action
    for definition in GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS.values()
    for action in definition['actions']
}


def get_group_level_actions_model(
    subject: str,
) -> Set[str]:
    if subject.endswith(FLUID_IDENTIFIER):
        return GROUP_LEVEL_ACTIONS_FOR_FLUIDATTACKS
    return GROUP_LEVEL_ACTIONS


def get_group_level_roles_model(
    subject: str,
) -> Dict[str, Dict[str, Set[str]]]:
    if subject.endswith(FLUID_IDENTIFIER):
        return GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS
    return GROUP_LEVEL_ROLES


# Map(role_name -> Map(actions|tags -> definition))
ORGANIZATION_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            'backend_api_mutations_create_group_mutate',
            'backend_api_mutations_edit_stakeholder_organization_mutate',
            (
                'backend_api_mutations_grant_stakeholder_'
                'organization_access_mutate'
            ),
            (
                'backend_api_mutations_remove_stakeholder_'
                'organization_access_mutate'
            ),
            'backend_api_mutations_update_organization_policies_mutate',
            'backend_api_resolvers_organization_analytics_resolve',
            'backend_api_resolvers_organization_stakeholders_resolve',
            (
                'backend_api_resolvers_query_stakeholder__'
                'resolve_for_organization'
            ),
            'grant_organization_level_role:customer',
            'grant_organization_level_role:customeradmin',
        },
        tags=set()
    ),
    customer=dict(
        actions={
            'backend_api_resolvers_organization_analytics_resolve',
        },
        tags=set()
    ),
    customeradmin=dict(
        actions={
            'backend_api_mutations_edit_stakeholder_organization_mutate',
            (
                'backend_api_mutations_grant_stakeholder_'
                'organization_access_mutate'
            ),
            (
                'backend_api_mutations_remove_stakeholder_'
                'organization_access_mutate'
            ),
            'backend_api_mutations_update_organization_policies_mutate',
            'backend_api_resolvers_organization_analytics_resolve',
            'backend_api_resolvers_organization_stakeholders_resolve',
            (
                'backend_api_resolvers_query_stakeholder_'
                '_resolve_for_organization'
            ),
            'grant_organization_level_role:customer',
            'grant_organization_level_role:customeradmin',
        },
        tags=set()
    ),
    group_manager=dict(
        actions={
            'backend_api_mutations_edit_stakeholder_organization_mutate',
            (
                'backend_api_mutations_grant_stakeholder_'
                'organization_access_mutate'
            ),
            (
                'backend_api_mutations_remove_stakeholder_'
                'organization_access_mutate'
            ),
            'backend_api_resolvers_organization_analytics_resolve',
            'backend_api_resolvers_organization_stakeholders_resolve',
            (
                'backend_api_resolvers_query_stakeholder_'
                '_resolve_for_organization'
            ),
        },
        tags=set()
    )
)

# Map(role_name -> Map(actions|tags -> definition))
ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS: Dict[
    str, Dict[str, Set[str]]
] = dict(
    admin=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES['admin']['actions'],
            'grant_organization_level_role:group_manager',
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES['admin']['tags'],
        }
    ),
    customer=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES['customer']['actions'],
            'backend_api_mutations_create_group_mutate',
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES['customer']['tags'],
        }
    ),
    customeradmin=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES['customeradmin']['actions'],
            'backend_api_mutations_create_group_mutate',
            'grant_organization_level_role:group_manager',
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES['customeradmin']['tags'],
        }
    ),
    group_manager=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES['group_manager']['actions'],
            'backend_api_mutations_create_group_mutate',
            'grant_organization_level_role:group_manager',
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES['group_manager']['tags'],
        }
    )
)

ORGANIZATION_LEVEL_ACTIONS: Set[str] = {
    action
    for definition in ORGANIZATION_LEVEL_ROLES.values()
    for action in definition['actions']
}

ORGANIZATION_LEVEL_ACTIONS_FOR_FLUIDATTACKS: Set[str] = {
    action
    for definition in ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS.values()
    for action in definition['actions']
}


def get_organization_level_actions_model(
    subject: str,
) -> Set[str]:
    if subject.endswith(FLUID_IDENTIFIER):
        return ORGANIZATION_LEVEL_ACTIONS_FOR_FLUIDATTACKS
    return ORGANIZATION_LEVEL_ACTIONS


def get_organization_level_roles_model(
    subject: str,
) -> Dict[str, Dict[str, Set[str]]]:
    if subject.endswith(FLUID_IDENTIFIER):
        return ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS
    return ORGANIZATION_LEVEL_ROLES


# Map(role_name -> Map(actions|tags -> definition))
USER_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            'backend_api_mutations_add_stakeholder_mutate',
            'backend_api_mutations_create_group_mutate',
            'backend_api_mutations_create_organization_mutate',
            'backend_api_mutations_invalidate_cache_mutate',
            'backend_api_resolvers_query_groups_resolve',
            'backend_api_resolvers_query_internal_names_resolve',
            'backend_api_resolvers_query_report__get_url_all_users',
            'backend_api_resolvers_query_report__get_url_all_vulns',
            'backend_api_resolvers_query_user_list_groups_resolve',
            'backend_api_resolvers_query_projects_with_forces_resolve',
            'front_can_use_groups_searchbar',
            'grant_user_level_role:admin',
            'grant_user_level_role:analyst',
            'grant_user_level_role:customer',
        },
        tags=set(),
    ),
    analyst=dict(
        actions={
            'backend_api_resolvers_query_internal_names_resolve',
        },
        tags={
            'drills',
        },
    ),
    customer=dict(
        actions={
            'backend_api_resolvers_query_internal_names_resolve',
        },
        tags=set(),
    ),
)

# Map(role_name -> Map(actions|tags -> definition))
USER_LEVEL_ROLES_FOR_FLUIDATTACKS: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            *USER_LEVEL_ROLES['admin']['actions'],
        },
        tags={
            *USER_LEVEL_ROLES['admin']['tags'],
        }
    ),
    analyst=dict(
        actions={
            *USER_LEVEL_ROLES['analyst']['actions'],
            'backend_api_mutations_create_group_mutate',
            'backend_api_mutations_create_organization_mutate',
            'backend_api_resolvers_query_user_list_groups_resolve',
            'front_can_use_groups_searchbar',
        },
        tags={
            *USER_LEVEL_ROLES['analyst']['tags'],
        }
    ),
    customer=dict(
        actions={
            *USER_LEVEL_ROLES['customer']['actions'],
            'backend_api_mutations_create_group_mutate',
            'backend_api_mutations_create_organization_mutate',
            'front_can_use_groups_searchbar',
        },
        tags={
            *USER_LEVEL_ROLES['customer']['tags'],
        }
    ),
)

USER_LEVEL_ACTIONS: Set[str] = {
    action
    for definition in USER_LEVEL_ROLES.values()
    for action in definition['actions']
}

USER_LEVEL_ACTIONS_FOR_FLUIDATTACKS: Set[str] = {
    action
    for definition in USER_LEVEL_ROLES_FOR_FLUIDATTACKS.values()
    for action in definition['actions']
}


def get_user_level_actions_model(
    subject: str,
) -> Set[str]:
    if subject.endswith(FLUID_IDENTIFIER):
        return USER_LEVEL_ACTIONS_FOR_FLUIDATTACKS
    return USER_LEVEL_ACTIONS


def get_user_level_roles_model(
    subject: str,
) -> Dict[str, Dict[str, Set[str]]]:
    if subject.endswith(FLUID_IDENTIFIER):
        return USER_LEVEL_ROLES_FOR_FLUIDATTACKS
    return USER_LEVEL_ROLES


# Map(service -> feature)
SERVICE_ATTRIBUTES: Dict[str, Set[str]] = dict(
    continuous={
        'is_continuous',
    },
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
