from typing import (
    Dict,
    Set,
)


# Constants
FLUID_IDENTIFIER = "@fluidattacks.com"
RoleModel = Dict[str, Dict[str, Set[str]]]

# Map(role_name -> Map(actions|tags -> definition))
GROUP_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            "api_mutations_activate_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_approve_draft_mutate",
            "api_mutations_confirm_zero_risk_vuln_mutate",
            "api_mutations_create_draft_mutate",
            "api_mutations_create_draft_new_mutate",
            "api_mutations_create_event_mutate",
            "api_mutations_deactivate_root_mutate",
            "api_mutations_delete_finding_mutate",
            "api_mutations_delete_vulnerability_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_download_vulnerability_file_mutate",
            "api_mutations_edit_group_mutate",
            "api_mutations_edit_stakeholder_mutate",
            "api_mutations_grant_stakeholder_access_mutate",
            "api_mutations_reject_draft_mutate",
            "api_mutations_reject_zero_risk_vuln_mutate",
            "api_mutations_remove_event_evidence_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_finding_evidence_mutate",
            "api_mutations_remove_group_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_remove_stakeholder_access_mutate",
            "api_mutations_request_verification_vulnerability_mutate",
            "api_mutations_request_zero_risk_vuln_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_submit_draft_mutate",
            "api_mutations_submit_draft_new_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_event_evidence_mutate",
            "api_mutations_update_evidence_description_mutate",
            "api_mutations_update_evidence_mutate",
            "api_mutations_update_finding_description_mutate",
            "api_mutations_update_forces_access_token_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_root_cloning_status_mutate",
            "api_mutations_update_root_state_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_severity_mutate",
            "api_mutations_update_vuln_commit_mutate",
            "api_mutations_upload_file_mutate",
            "api_mutations_verify_request_vulnerability_mutate",
            "api_resolvers_finding__do_add_finding_consult",
            "api_resolvers_finding_analyst_resolve",
            "api_resolvers_finding_historic_state_resolve",
            "api_resolvers_finding_new_historic_state_new_resolve",
            "api_resolvers_finding_new_observations_new_resolve",
            "api_resolvers_finding_new_sorts_new_resolve",
            "api_resolvers_finding_new_zero_risk_new_resolve",
            "api_resolvers_finding_observations_resolve",
            "api_resolvers_finding_sorts_resolve",
            "api_resolvers_finding_zero_risk_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_bill_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_drafts_resolve",
            "api_resolvers_group_forces_token_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_group_stakeholders_resolve",
            "api_resolvers_organization__do_move_group_organization",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_report__get_url_group_report",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_stakeholder__resolve_for_group",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_analyst_resolve",
            "api_resolvers_vulnerability_historic_verification_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
            "grant_group_level_role:analyst",
            "grant_group_level_role:closer",
            "grant_group_level_role:customer",
            "grant_group_level_role:customeradmin",
            "grant_group_level_role:executive",
            "grant_group_level_role:group_manager",
            "grant_group_level_role:resourcer",
            "grant_group_level_role:reviewer",
            "post_finding_observation",
            "update_git_root_filter",
        },
        tags=set(),
    ),
    analyst=dict(
        actions={
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_create_draft_mutate",
            "api_mutations_create_draft_new_mutate",
            "api_mutations_create_event_mutate",
            "api_mutations_delete_finding_mutate",
            "api_mutations_delete_vulnerability_mutate",
            "api_mutations_delete_vulnerability_tags_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_download_vulnerability_file_mutate",
            "api_mutations_reject_draft_mutate",
            "api_mutations_remove_event_evidence_mutate",
            "api_mutations_remove_finding_evidence_mutate",
            "api_mutations_request_verification_vulnerability_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_submit_draft_mutate",
            "api_mutations_submit_draft_new_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_event_evidence_mutate",
            "api_mutations_update_evidence_description_mutate",
            "api_mutations_update_evidence_mutate",
            "api_mutations_update_finding_description_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_treatment_vulnerability_mutate",
            "api_mutations_update_severity_mutate",
            "api_mutations_upload_file_mutate",
            "api_mutations_verify_request_vulnerability_mutate",
            "api_resolvers_finding__do_add_finding_consult",
            "api_resolvers_finding_analyst_resolve",
            "api_resolvers_finding_historic_state_resolve",
            "api_resolvers_finding_new_historic_state_new_resolve",
            "api_resolvers_finding_new_observations_new_resolve",
            "api_resolvers_finding_new_sorts_new_resolve",
            "api_resolvers_finding_observations_resolve",
            "api_resolvers_finding_sorts_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_drafts_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_report__get_url_group_report",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_analyst_resolve",
            "api_resolvers_vulnerability_historic_verification_resolve",
            "post_finding_observation",
        },
        tags={
            "drills",
        },
    ),
    closer=dict(
        actions={
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_create_draft_mutate",
            "api_mutations_create_draft_new_mutate",
            "api_mutations_create_event_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_download_vulnerability_file_mutate",
            "api_mutations_remove_finding_evidence_mutate",
            "api_mutations_reject_draft_mutate",
            "api_mutations_request_verification_vulnerability_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_submit_draft_mutate",
            "api_mutations_submit_draft_new_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_evidence_description_mutate",
            "api_mutations_update_evidence_mutate",
            "api_mutations_update_finding_description_mutate",
            "api_mutations_update_root_cloning_status_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_upload_file_mutate",
            "api_mutations_verify_request_vulnerability_mutate",
            "api_resolvers_finding__do_add_finding_consult",
            "api_resolvers_finding_analyst_resolve",
            "api_resolvers_finding_historic_state_resolve",
            "api_resolvers_finding_new_historic_state_new_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_drafts_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_analyst_resolve",
            "api_resolvers_vulnerability_historic_verification_resolve",
        },
        tags={
            "drills",
        },
    ),
    customer=dict(
        actions={
            "api_resolvers_group_forces_token_resolve",
            "api_mutations_update_forces_access_token_mutate",
            "api_mutations_activate_root_mutate",
            "api_mutations_deactivate_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_delete_vulnerability_tags_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_request_verification_vulnerability_mutate",
            "api_mutations_request_zero_risk_vuln_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_root_state_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_treatment_vulnerability_mutate",
            "api_mutations_update_vulns_treatment_mutate",
            "api_resolvers_finding__do_add_finding_consult",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_bill_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
            "update_git_root_filter",
            "valid_treatment_manager",
        },
        tags=set(),
    ),
    customeradmin=dict(
        actions={
            "api_resolvers_group_forces_token_resolve",
            "api_mutations_update_forces_access_token_mutate",
            "api_mutations_activate_root_mutate",
            "api_mutations_deactivate_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_delete_vulnerability_tags_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_edit_group_mutate",
            "api_mutations_edit_stakeholder_mutate",
            "api_mutations_grant_stakeholder_access_mutate",
            "api_mutations_handle_vulns_acceptation_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_group_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_remove_stakeholder_access_mutate",
            "api_mutations_request_verification_vulnerability_mutate",
            "api_mutations_request_zero_risk_vuln_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_root_state_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_treatment_vulnerability_mutate",
            "api_mutations_update_vulns_treatment_mutate",
            "api_resolvers_finding__do_add_finding_consult",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_bill_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_group_stakeholders_resolve",
            "api_resolvers_organization__do_move_group_organization",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_report__get_url_group_report",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_stakeholder__resolve_for_group",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
            "grant_group_level_role:customer",
            "grant_group_level_role:customeradmin",
            "grant_group_level_role:executive",
            "grant_user_level_role:customer",
            "update_git_root_filter",
            "valid_treatment_manager",
        },
        tags=set(),
    ),
    executive=dict(
        actions={
            "api_mutations_activate_root_mutate",
            "api_mutations_deactivate_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_delete_vulnerability_tags_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_request_verification_vulnerability_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_root_state_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_treatment_vulnerability_mutate",
            "api_mutations_update_vulns_treatment_mutate",
            "api_resolvers_finding__do_add_finding_consult",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_vulnerability_resolve",
        },
        tags=set(),
    ),
    group_manager=dict(
        actions={
            "api_resolvers_group_forces_token_resolve",
            "api_mutations_update_forces_access_token_mutate",
            "api_mutations_activate_root_mutate",
            "api_mutations_deactivate_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_create_event_mutate",
            "api_mutations_delete_vulnerability_tags_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_edit_group_mutate",
            "api_mutations_edit_stakeholder_mutate",
            "api_mutations_grant_stakeholder_access_mutate",
            "api_mutations_handle_vulns_acceptation_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_group_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_remove_stakeholder_access_mutate",
            "api_mutations_request_verification_vulnerability_mutate",
            "api_mutations_request_zero_risk_vuln_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_forces_access_token_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_root_state_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_treatment_vulnerability_mutate",
            "api_mutations_update_vulns_treatment_mutate",
            "api_mutations_update_forces_access_token_mutate",
            "api_resolvers_finding__do_add_finding_consult",
            "api_resolvers_finding_analyst_resolve",
            "api_resolvers_finding_new_observations_new_resolve",
            "api_resolvers_finding_observations_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_bill_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_drafts_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_group_stakeholders_resolve",
            "api_resolvers_organization__do_move_group_organization",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_report__get_url_group_report",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_stakeholder__resolve_for_group",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_analyst_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
            "grant_group_level_role:analyst",
            "grant_group_level_role:closer",
            "grant_group_level_role:customer",
            "grant_group_level_role:customeradmin",
            "grant_group_level_role:executive",
            "grant_group_level_role:group_manager",
            "grant_group_level_role:resourcer",
            "grant_group_level_role:reviewer",
            "grant_user_level_role:customer",
            "post_finding_observation",
            "update_git_root_filter",
            "valid_treatment_manager",
        },
        tags=set(),
    ),
    resourcer=dict(
        actions={
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_create_event_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_request_verification_vulnerability_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_root_cloning_status_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_vulnerability_resolve",
            "update_git_root_filter",
        },
        tags={
            "drills",
        },
    ),
    reviewer=dict(
        actions={
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_approve_draft_mutate",
            "api_mutations_confirm_zero_risk_vuln_mutate",
            "api_mutations_delete_finding_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_reject_draft_mutate",
            "api_mutations_reject_zero_risk_vuln_mutate",
            "api_mutations_request_verification_vulnerability_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_evidence_description_mutate",
            "api_mutations_update_finding_description_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_severity_mutate",
            "api_mutations_upload_file_mutate",
            "api_resolvers_finding__do_add_finding_consult",
            "api_resolvers_finding_analyst_resolve",
            "api_resolvers_finding_historic_state_resolve",
            "api_resolvers_finding_new_historic_state_new_resolve",
            "api_resolvers_finding_new_observations_new_resolve",
            "api_resolvers_finding_new_zero_risk_new_resolve",
            "api_resolvers_finding_observations_resolve",
            "api_resolvers_finding_zero_risk_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_drafts_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_group_stakeholders_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_stakeholder__resolve_for_group",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_analyst_resolve",
            "api_resolvers_vulnerability_historic_verification_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
            "handle_comment_scope",
            "post_finding_observation",
            "see_dropdown_to_confirm_zero_risk",
            "see_dropdown_to_reject_zero_risk",
        },
        tags={
            "drills",
        },
    ),
    service_forces=dict(
        actions={
            "api_mutations_add_forces_execution_mutate",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
        },
        tags={"forces"},
    ),
)

# Map(role_name -> Map(actions|tags -> definition))
GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            *GROUP_LEVEL_ROLES["admin"]["actions"],
            "api_resolvers_finding_new_analyst_new_resolve",
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["admin"]["tags"],
        },
    ),
    analyst=dict(
        actions={
            *GROUP_LEVEL_ROLES["analyst"]["actions"],
            "api_resolvers_finding_new_analyst_new_resolve",
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["analyst"]["tags"],
        },
    ),
    closer=dict(
        actions={
            *GROUP_LEVEL_ROLES["closer"]["actions"],
            "api_resolvers_finding_new_analyst_new_resolve",
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["closer"]["tags"],
        },
    ),
    customer=dict(
        actions={
            *GROUP_LEVEL_ROLES["customer"]["actions"],
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["customer"]["tags"],
        },
    ),
    customeradmin=dict(
        actions={
            *GROUP_LEVEL_ROLES["customeradmin"]["actions"],
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["customeradmin"]["tags"],
        },
    ),
    executive=dict(
        actions={
            *GROUP_LEVEL_ROLES["executive"]["actions"],
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["executive"]["tags"],
        },
    ),
    group_manager=dict(
        actions={
            *GROUP_LEVEL_ROLES["group_manager"]["actions"],
            "api_resolvers_finding_new_analyst_new_resolve",
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["group_manager"]["tags"],
        },
    ),
    resourcer=dict(
        actions={
            *GROUP_LEVEL_ROLES["resourcer"]["actions"],
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["resourcer"]["tags"],
        },
    ),
    reviewer=dict(
        actions={
            *GROUP_LEVEL_ROLES["reviewer"]["actions"],
            "api_resolvers_finding_new_analyst_new_resolve",
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["reviewer"]["tags"],
        },
    ),
    # Do not add more authz since users which pay for the forces service
    # could impersonate a fluidattacks user
    service_forces=dict(
        **GROUP_LEVEL_ROLES["service_forces"],
    ),
)


# Map(role_name -> Map(actions|tags -> definition))
ORGANIZATION_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            "api_mutations_create_group_mutate",
            "api_mutations_edit_stakeholder_organization_mutate",
            "api_mutations_grant_stakeholder_organization_access_mutate",
            "api_mutations_remove_stakeholder_organization_access_mutate",
            "api_mutations_update_organization_policies_mutate",
            "api_resolvers_organization_analytics_resolve",
            "api_resolvers_organization_stakeholders_resolve",
            "api_resolvers_query_stakeholder__resolve_for_organization",
            "grant_organization_level_role:customer",
            "grant_organization_level_role:customeradmin",
        },
        tags=set(),
    ),
    customer=dict(
        actions={
            "api_mutations_add_org_finding_policy_mutate",
            "api_resolvers_organization_analytics_resolve",
        },
        tags=set(),
    ),
    customeradmin=dict(
        actions={
            "api_mutations_add_org_finding_policy_mutate",
            "api_mutations_deactivate_finding_policy_mutate",
            "api_mutations_handle_finding_policy_acceptation_mutate",
            "api_mutations_edit_stakeholder_organization_mutate",
            "api_mutations_grant_stakeholder_organization_access_mutate",
            "api_mutations_remove_stakeholder_organization_access_mutate",
            "api_mutations_update_organization_policies_mutate",
            "api_resolvers_organization_analytics_resolve",
            "api_resolvers_organization_stakeholders_resolve",
            "api_resolvers_query_stakeholder__resolve_for_organization",
            "grant_organization_level_role:customer",
            "grant_organization_level_role:customeradmin",
        },
        tags=set(),
    ),
    group_manager=dict(
        actions={
            "api_mutations_add_org_finding_policy_mutate",
            "api_mutations_deactivate_finding_policy_mutate",
            "api_mutations_handle_finding_policy_acceptation_mutate",
            "api_mutations_edit_stakeholder_organization_mutate",
            "api_mutations_grant_stakeholder_organization_access_mutate",
            "api_mutations_remove_stakeholder_organization_access_mutate",
            "api_resolvers_organization_analytics_resolve",
            "api_resolvers_organization_stakeholders_resolve",
            "api_resolvers_query_stakeholder__resolve_for_organization",
        },
        tags=set(),
    ),
)

# Map(role_name -> Map(actions|tags -> definition))
ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS: Dict[
    str, Dict[str, Set[str]]
] = dict(
    admin=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES["admin"]["actions"],
            "grant_organization_level_role:group_manager",
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES["admin"]["tags"],
        },
    ),
    customer=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES["customer"]["actions"],
            "api_mutations_create_group_mutate",
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES["customer"]["tags"],
        },
    ),
    customeradmin=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES["customeradmin"]["actions"],
            "api_mutations_create_group_mutate",
            "grant_organization_level_role:group_manager",
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES["customeradmin"]["tags"],
        },
    ),
    group_manager=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES["group_manager"]["actions"],
            "api_mutations_create_group_mutate",
            "grant_organization_level_role:group_manager",
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES["group_manager"]["tags"],
        },
    ),
)


# Map(role_name -> Map(actions|tags -> definition))
USER_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            "api_mutations_add_stakeholder_mutate",
            "api_mutations_create_group_mutate",
            "api_mutations_create_organization_mutate",
            "api_mutations_invalidate_cache_mutate",
            "api_resolvers_query_groups_resolve",
            "api_resolvers_query_internal_names_resolve",
            "api_resolvers_query_user_list_groups_resolve",
            "api_resolvers_query_groups_with_forces_resolve",
            "front_can_use_groups_searchbar",
            "grant_user_level_role:admin",
            "grant_user_level_role:analyst",
            "grant_user_level_role:customer",
        },
        tags=set(),
    ),
    analyst=dict(
        actions={
            "api_resolvers_query_internal_names_resolve",
        },
        tags={
            "drills",
        },
    ),
    customer=dict(
        actions={
            "api_resolvers_query_internal_names_resolve",
        },
        tags=set(),
    ),
)

# Map(role_name -> Map(actions|tags -> definition))
USER_LEVEL_ROLES_FOR_FLUIDATTACKS: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            *USER_LEVEL_ROLES["admin"]["actions"],
            "keep_default_organization_access",
        },
        tags={
            *USER_LEVEL_ROLES["admin"]["tags"],
        },
    ),
    analyst=dict(
        actions={
            *USER_LEVEL_ROLES["analyst"]["actions"],
            "api_mutations_create_group_mutate",
            "api_mutations_create_organization_mutate",
            "api_resolvers_query_user_list_groups_resolve",
            "front_can_use_groups_searchbar",
            "keep_default_organization_access",
        },
        tags={
            *USER_LEVEL_ROLES["analyst"]["tags"],
        },
    ),
    customer=dict(
        actions={
            *USER_LEVEL_ROLES["customer"]["actions"],
            "api_mutations_create_group_mutate",
            "api_mutations_create_organization_mutate",
            "front_can_use_groups_searchbar",
            "keep_default_organization_access",
        },
        tags={
            *USER_LEVEL_ROLES["customer"]["tags"],
        },
    ),
)

# Map(service -> feature)
SERVICE_ATTRIBUTES: Dict[str, Set[str]] = dict(
    continuous={
        "is_continuous",
    },
    drills_black={
        "has_drills_black",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    },
    drills_white={
        "has_drills_white",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    },
    forces={
        "has_forces",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    },
    integrates={
        "has_integrates",
    },
)

# Actions
GROUP_LEVEL_ACTIONS: Set[str] = {
    action
    for definition in GROUP_LEVEL_ROLES.values()
    for action in definition["actions"]
}
GROUP_LEVEL_ACTIONS_FOR_FLUIDATTACKS: Set[str] = {
    action
    for definition in GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS.values()
    for action in definition["actions"]
}

ORGANIZATION_LEVEL_ACTIONS: Set[str] = {
    action
    for definition in ORGANIZATION_LEVEL_ROLES.values()
    for action in definition["actions"]
}
ORGANIZATION_LEVEL_ACTIONS_FOR_FLUIDATTACKS: Set[str] = {
    action
    for definition in ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS.values()
    for action in definition["actions"]
}

USER_LEVEL_ACTIONS: Set[str] = {
    action
    for definition in USER_LEVEL_ROLES.values()
    for action in definition["actions"]
}
USER_LEVEL_ACTIONS_FOR_FLUIDATTACKS: Set[str] = {
    action
    for definition in USER_LEVEL_ROLES_FOR_FLUIDATTACKS.values()
    for action in definition["actions"]
}

SERVICE_ATTRIBUTES_SET: Set[str] = {
    action for actions in SERVICE_ATTRIBUTES.values() for action in actions
}


def get_group_level_actions_model(subject: str) -> Set[str]:
    if subject.endswith(FLUID_IDENTIFIER):
        return GROUP_LEVEL_ACTIONS_FOR_FLUIDATTACKS
    return GROUP_LEVEL_ACTIONS


def get_group_level_roles_model(subject: str) -> RoleModel:
    if subject.endswith(FLUID_IDENTIFIER):
        return GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS
    return GROUP_LEVEL_ROLES


def get_organization_level_actions_model(subject: str) -> Set[str]:
    if subject.endswith(FLUID_IDENTIFIER):
        return ORGANIZATION_LEVEL_ACTIONS_FOR_FLUIDATTACKS
    return ORGANIZATION_LEVEL_ACTIONS


def get_organization_level_roles_model(subject: str) -> RoleModel:
    if subject.endswith(FLUID_IDENTIFIER):
        return ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS
    return ORGANIZATION_LEVEL_ROLES


def get_user_level_actions_model(subject: str) -> Set[str]:
    if subject.endswith(FLUID_IDENTIFIER):
        return USER_LEVEL_ACTIONS_FOR_FLUIDATTACKS
    return USER_LEVEL_ACTIONS


def get_user_level_roles_model(
    subject: str,
) -> RoleModel:
    if subject.endswith(FLUID_IDENTIFIER):
        return USER_LEVEL_ROLES_FOR_FLUIDATTACKS
    return USER_LEVEL_ROLES
