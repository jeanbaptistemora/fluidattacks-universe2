# pylint: disable=too-many-lines

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
            "api_mutations_add_draft_mutate",
            "api_mutations_add_draft_new_mutate",
            "api_mutations_add_event_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_files_to_db_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_approve_draft_mutate",
            "api_mutations_approve_draft_new_mutate",
            "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
            "api_mutations_deactivate_root_mutate",
            "api_mutations_move_root_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_download_vulnerability_file_mutate",
            "api_mutations_update_group_mutate",
            "api_mutations_update_group_stakeholder_mutate",
            "api_mutations_grant_stakeholder_access_mutate",
            "api_mutations_reject_draft_mutate",
            "api_mutations_reject_draft_new_mutate",
            "api_mutations_reject_vulnerabilities_zero_risk_mutate",
            "api_mutations_reject_vulnerabilities_zero_risk_new_mutate",
            "api_mutations_remove_finding_mutate",
            "api_mutations_remove_finding_new_mutate",
            "api_mutations_remove_event_evidence_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_finding_evidence_mutate",
            "api_mutations_remove_finding_evidence_new_mutate",
            "api_mutations_remove_group_mutate",
            "api_mutations_remove_group_new_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_remove_stakeholder_access_mutate",
            "api_mutations_remove_vulnerability_mutate",
            "api_mutations_remove_vulnerability_new_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_new_mutate",
            "api_mutations_request_vulnerabilities_zero_risk_mutate",
            "api_mutations_request_vulnerabilities_zero_risk_new_mutate",
            "api_mutations_sign_post_url_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_submit_draft_mutate",
            "api_mutations_submit_draft_new_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_event_evidence_mutate",
            "api_mutations_update_evidence_description_mutate",
            "api_mutations_update_evidence_description_new_mutate",
            "api_mutations_update_evidence_mutate",
            "api_mutations_update_evidence_new_mutate",
            "api_mutations_update_finding_description_mutate",
            "api_mutations_update_finding_description_new_mutate",
            "api_mutations_update_forces_access_token_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_root_cloning_status_mutate",
            "api_mutations_update_root_state_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_severity_mutate",
            "api_mutations_update_severity_new_mutate",
            "api_mutations_update_vulnerability_commit_mutate",
            "api_mutations_update_vulnerability_commit_new_mutate",
            "api_mutations_upload_file_mutate",
            "api_mutations_upload_file_new_mutate",
            "api_mutations_verify_vulnerabilities_request_mutate",
            "api_mutations_verify_vulnerabilities_request_new_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_finding_hacker_resolve",
            "api_resolvers_finding_historic_state_resolve",
            "api_resolvers_finding_new_consulting_new_resolve",
            "api_resolvers_finding_new_hacker_new_resolve",
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
            "api_resolvers_group_drafts_new_resolve",
            "api_resolvers_group_forces_token_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_group_stakeholders_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_finding_new__get_draft",
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
            "api_resolvers_vulnerability_hacker_resolve",
            "api_resolvers_vulnerability_historic_verification_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
            "api_resolvers_query_vulnerability_new_resolve",
            "api_resolvers_vulnerability_new_hacker_resolve",
            "api_resolvers_vulnerability_new_historic_verification_resolve",
            "api_resolvers_vulnerability_new_historic_zero_risk_resolve",
            "grant_group_level_role:customer",
            "grant_group_level_role:customeradmin",
            "grant_group_level_role:executive",
            "grant_group_level_role:hacker",
            "grant_group_level_role:reattacker",
            "grant_group_level_role:resourcer",
            "grant_group_level_role:reviewer",
            "grant_group_level_role:system_owner",
            "post_finding_observation",
            "update_git_root_filter",
        },
        tags=set(),
    ),
    hacker=dict(
        actions={
            "api_mutations_add_draft_mutate",
            "api_mutations_add_draft_new_mutate",
            "api_mutations_add_event_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_download_vulnerability_file_mutate",
            "api_mutations_remove_event_evidence_mutate",
            "api_mutations_remove_finding_mutate",
            "api_mutations_remove_finding_new_mutate",
            "api_mutations_remove_finding_evidence_mutate",
            "api_mutations_remove_finding_evidence_new_mutate",
            "api_mutations_remove_vulnerability_mutate",
            "api_mutations_remove_vulnerability_new_mutate",
            "api_mutations_remove_vulnerability_tags_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_new_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_submit_draft_mutate",
            "api_mutations_submit_draft_new_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_event_evidence_mutate",
            "api_mutations_update_evidence_description_mutate",
            "api_mutations_update_evidence_description_new_mutate",
            "api_mutations_update_evidence_mutate",
            "api_mutations_update_evidence_new_mutate",
            "api_mutations_update_finding_description_mutate",
            "api_mutations_update_finding_description_new_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_vulnerability_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_new_mutate",
            "api_mutations_update_severity_mutate",
            "api_mutations_update_severity_new_mutate",
            "api_mutations_upload_file_mutate",
            "api_mutations_upload_file_new_mutate",
            "api_mutations_verify_vulnerabilities_request_mutate",
            "api_mutations_verify_vulnerabilities_request_new_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_finding_hacker_resolve",
            "api_resolvers_finding_historic_state_resolve",
            "api_resolvers_finding_new_consulting_new_resolve",
            "api_resolvers_finding_new_hacker_new_resolve",
            "api_resolvers_finding_new_historic_state_new_resolve",
            "api_resolvers_finding_new_observations_new_resolve",
            "api_resolvers_finding_new_sorts_new_resolve",
            "api_resolvers_finding_observations_resolve",
            "api_resolvers_finding_sorts_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_drafts_resolve",
            "api_resolvers_group_drafts_new_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_finding_new__get_draft",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_report__get_url_group_report",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_hacker_resolve",
            "api_resolvers_vulnerability_historic_verification_resolve",
            "post_finding_observation",
        },
        tags={
            "drills",
        },
    ),
    reattacker=dict(
        actions={
            "api_mutations_add_draft_mutate",
            "api_mutations_add_draft_new_mutate",
            "api_mutations_add_event_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_download_vulnerability_file_mutate",
            "api_mutations_remove_finding_evidence_mutate",
            "api_mutations_remove_finding_evidence_new_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_new_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_submit_draft_mutate",
            "api_mutations_submit_draft_new_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_evidence_description_mutate",
            "api_mutations_update_evidence_description_new_mutate",
            "api_mutations_update_evidence_mutate",
            "api_mutations_update_evidence_new_mutate",
            "api_mutations_update_finding_description_mutate",
            "api_mutations_update_finding_description_new_mutate",
            "api_mutations_update_root_cloning_status_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_upload_file_mutate",
            "api_mutations_upload_file_new_mutate",
            "api_mutations_verify_vulnerabilities_request_mutate",
            "api_mutations_verify_vulnerabilities_request_new_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_finding_hacker_resolve",
            "api_resolvers_finding_historic_state_resolve",
            "api_resolvers_finding_new_consulting_new_resolve",
            "api_resolvers_finding_new_hacker_new_resolve",
            "api_resolvers_finding_new_historic_state_new_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_drafts_resolve",
            "api_resolvers_group_drafts_new_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_finding_new__get_draft",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_hacker_resolve",
            "api_resolvers_vulnerability_historic_verification_resolve",
        },
        tags={
            "drills",
        },
    ),
    customer=dict(
        actions={
            "api_mutations_activate_root_mutate",
            "api_mutations_deactivate_root_mutate",
            "api_mutations_update_root_state_mutate",
            "api_resolvers_group_forces_token_resolve",
            "api_mutations_update_forces_access_token_mutate",
            "api_mutations_move_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_files_to_db_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_remove_vulnerability_tags_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_new_mutate",
            "api_mutations_request_vulnerabilities_zero_risk_mutate",
            "api_mutations_request_vulnerabilities_zero_risk_new_mutate",
            "api_mutations_sign_post_url_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_vulnerability_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_new_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_finding_new_consulting_new_resolve",
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
            "api_mutations_move_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_files_to_db_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_update_group_mutate",
            "api_mutations_update_group_stakeholder_mutate",
            "api_mutations_grant_stakeholder_access_mutate",
            "api_mutations_handle_vulns_acceptation_mutate",
            "api_mutations_handle_vulnerabilities_acceptation_mutate",
            "api_mutations_handle_vulnerabilities_acceptation_new_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_group_mutate",
            "api_mutations_remove_group_new_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_remove_stakeholder_access_mutate",
            "api_mutations_remove_vulnerability_tags_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_new_mutate",
            "api_mutations_request_vulnerabilities_zero_risk_mutate",
            "api_mutations_request_vulnerabilities_zero_risk_new_mutate",
            "api_mutations_sign_post_url_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_root_state_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_vulnerability_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_new_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_finding_new_consulting_new_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_bill_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_group_stakeholders_resolve",
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
            "api_mutations_update_root_state_mutate",
            "api_mutations_move_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_files_to_db_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_remove_vulnerability_tags_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_new_mutate",
            "api_mutations_sign_post_url_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_vulnerability_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_new_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_finding_new_consulting_new_resolve",
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
    system_owner=dict(
        actions={
            "api_resolvers_group_forces_token_resolve",
            "api_mutations_update_forces_access_token_mutate",
            "api_mutations_activate_root_mutate",
            "api_mutations_deactivate_root_mutate",
            "api_mutations_move_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_files_to_db_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_event_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_update_group_mutate",
            "api_mutations_update_group_stakeholder_mutate",
            "api_mutations_grant_stakeholder_access_mutate",
            "api_mutations_handle_vulns_acceptation_mutate",
            "api_mutations_handle_vulnerabilities_acceptation_mutate",
            "api_mutations_handle_vulnerabilities_acceptation_new_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_group_mutate",
            "api_mutations_remove_group_new_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_remove_stakeholder_access_mutate",
            "api_mutations_remove_vulnerability_tags_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_new_mutate",
            "api_mutations_request_vulnerabilities_zero_risk_mutate",
            "api_mutations_request_vulnerabilities_zero_risk_new_mutate",
            "api_mutations_sign_post_url_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_root_state_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_vulnerability_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_new_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_finding_new_consulting_new_resolve",
            "api_resolvers_finding_hacker_resolve",
            "api_resolvers_finding_new_hacker_new_resolve",
            "api_resolvers_finding_new_observations_new_resolve",
            "api_resolvers_finding_observations_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_bill_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_drafts_resolve",
            "api_resolvers_group_drafts_new_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_group_stakeholders_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_finding_new__get_draft",
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
            "api_resolvers_vulnerability_hacker_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
            "grant_group_level_role:customer",
            "grant_group_level_role:customeradmin",
            "grant_group_level_role:executive",
            "grant_group_level_role:hacker",
            "grant_group_level_role:reattacker",
            "grant_group_level_role:resourcer",
            "grant_group_level_role:reviewer",
            "grant_user_level_role:customer",
            "grant_group_level_role:system_owner",
            "post_finding_observation",
            "valid_treatment_manager",
        },
        tags=set(),
    ),
    resourcer=dict(
        actions={
            "api_mutations_add_event_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_new_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_root_cloning_status_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_finding_new_consulting_new_resolve",
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
            "api_mutations_approve_draft_new_mutate",
            "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_reject_draft_mutate",
            "api_mutations_reject_draft_new_mutate",
            "api_mutations_reject_vulnerabilities_zero_risk_mutate",
            "api_mutations_reject_vulnerabilities_zero_risk_new_mutate",
            "api_mutations_remove_finding_mutate",
            "api_mutations_remove_finding_new_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_new_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_finding_hacker_resolve",
            "api_resolvers_finding_historic_state_resolve",
            "api_resolvers_finding_new_consulting_new_resolve",
            "api_resolvers_finding_new_hacker_new_resolve",
            "api_resolvers_finding_new_historic_state_new_resolve",
            "api_resolvers_finding_new_observations_new_resolve",
            "api_resolvers_finding_new_zero_risk_new_resolve",
            "api_resolvers_finding_observations_resolve",
            "api_resolvers_finding_zero_risk_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_drafts_resolve",
            "api_resolvers_group_drafts_new_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_group_stakeholders_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_finding_new__get_draft",
            "api_resolvers_query_finding_new_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_forces_executions_new_resolve",
            "api_resolvers_query_forces_executions_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_stakeholder__resolve_for_group",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_hacker_resolve",
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
# Permission duplication for the old roles
GROUP_LEVEL_ROLES["analyst"] = GROUP_LEVEL_ROLES["hacker"]
GROUP_LEVEL_ROLES["closer"] = GROUP_LEVEL_ROLES["reattacker"]
GROUP_LEVEL_ROLES["group_manager"] = GROUP_LEVEL_ROLES["system_owner"]

# Map(role_name -> Map(actions|tags -> definition))
GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            *GROUP_LEVEL_ROLES["admin"]["actions"],
            "api_mutations_submit_machine_job_mutate",
            "api_resolvers_finding_machine_jobs_resolve",
            "api_resolvers_finding_new_machine_jobs_new_resolve",
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["admin"]["tags"],
        },
    ),
    hacker=dict(
        actions={
            *GROUP_LEVEL_ROLES["hacker"]["actions"],
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["hacker"]["tags"],
        },
    ),
    reattacker=dict(
        actions={
            *GROUP_LEVEL_ROLES["reattacker"]["actions"],
            "api_mutations_submit_machine_job_mutate",
            "api_resolvers_finding_machine_jobs_resolve",
            "api_resolvers_finding_new_machine_jobs_new_resolve",
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["reattacker"]["tags"],
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
    system_owner=dict(
        actions={
            *GROUP_LEVEL_ROLES["system_owner"]["actions"],
            "api_mutations_submit_machine_job_mutate",
            "api_resolvers_finding_machine_jobs_resolve",
            "api_resolvers_finding_new_machine_jobs_new_resolve",
            "api_resolvers_finding_new_hacker_new_resolve",
            "api_resolvers_git_root_toe_lines_resolve",
            "api_resolvers_group_toe_inputs_resolve",
        },
        tags={
            *GROUP_LEVEL_ROLES["system_owner"]["tags"],
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
# Permission duplication for the old roles
GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS[
    "analyst"
] = GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS["hacker"]
GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS[
    "closer"
] = GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS["reattacker"]
GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS[
    "group_manager"
] = GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS["system_owner"]


# Map(role_name -> Map(actions|tags -> definition))
ORGANIZATION_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            "api_mutations_add_group_mutate",
            "api_mutations_update_organization_stakeholder_mutate",
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
            "api_mutations_add_organization_finding_policy_mutate",
            "api_mutations_submit_organization_finding_policy_mutate",
            "api_resolvers_organization_analytics_resolve",
        },
        tags=set(),
    ),
    customeradmin=dict(
        actions={
            "api_mutations_add_organization_finding_policy_mutate",
            "api_mutations_deactivate_finding_policy_mutate",
            "api_mutations_deactivate_organization_finding_policy_mutate",
            "api_mutations_handle_finding_policy_acceptation_mutate",
            (
                "api_mutations_handle_organization_finding_policy_acceptation_"
                "mutate"
            ),
            (
                "api_mutations_handle_organization_finding_policy_acceptance_"
                "mutate"
            ),
            "api_mutations_update_organization_stakeholder_mutate",
            "api_mutations_grant_stakeholder_organization_access_mutate",
            "api_mutations_remove_stakeholder_organization_access_mutate",
            "api_mutations_submit_organization_finding_policy_mutate",
            "api_mutations_update_organization_policies_mutate",
            "api_resolvers_organization_analytics_resolve",
            "api_resolvers_organization_stakeholders_resolve",
            "api_resolvers_query_stakeholder__resolve_for_organization",
            "grant_organization_level_role:customer",
            "grant_organization_level_role:customeradmin",
        },
        tags=set(),
    ),
    system_owner=dict(
        actions={
            "api_mutations_add_organization_finding_policy_mutate",
            "api_mutations_deactivate_finding_policy_mutate",
            "api_mutations_deactivate_organization_finding_policy_mutate",
            "api_mutations_handle_finding_policy_acceptation_mutate",
            (
                "api_mutations_handle_organization_finding_policy_acceptation_"
                "mutate"
            ),
            (
                "api_mutations_handle_organization_finding_policy_acceptance_"
                "mutate"
            ),
            "api_mutations_update_organization_stakeholder_mutate",
            "api_mutations_grant_stakeholder_organization_access_mutate",
            "api_mutations_remove_stakeholder_organization_access_mutate",
            "api_mutations_submit_organization_finding_policy_mutate",
            "api_resolvers_organization_analytics_resolve",
            "api_resolvers_organization_stakeholders_resolve",
            "api_resolvers_query_stakeholder__resolve_for_organization",
        },
        tags=set(),
    ),
)
# Permission duplication for the old roles
ORGANIZATION_LEVEL_ROLES["group_manager"] = ORGANIZATION_LEVEL_ROLES[
    "system_owner"
]


# Map(role_name -> Map(actions|tags -> definition))
ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS: Dict[
    str, Dict[str, Set[str]]
] = dict(
    admin=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES["admin"]["actions"],
            "grant_organization_level_role:system_owner",
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES["admin"]["tags"],
        },
    ),
    customer=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES["customer"]["actions"],
            "api_mutations_add_group_mutate",
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES["customer"]["tags"],
        },
    ),
    customeradmin=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES["customeradmin"]["actions"],
            "api_mutations_add_group_mutate",
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES["customeradmin"]["tags"],
        },
    ),
    system_owner=dict(
        actions={
            *ORGANIZATION_LEVEL_ROLES["system_owner"]["actions"],
            "api_mutations_add_group_mutate",
            "grant_organization_level_role:system_owner",
        },
        tags={
            *ORGANIZATION_LEVEL_ROLES["system_owner"]["tags"],
        },
    ),
)
# Permission duplication for the old roles
ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS[
    "group_manager"
] = ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS["system_owner"]


# Map(role_name -> Map(actions|tags -> definition))
USER_LEVEL_ROLES: Dict[str, Dict[str, Set[str]]] = dict(
    admin=dict(
        actions={
            "api_mutations_add_group_mutate",
            "api_mutations_add_organization_mutate",
            "api_mutations_add_stakeholder_mutate",
            "api_mutations_invalidate_cache_mutate",
            "api_resolvers_query_groups_resolve",
            "api_resolvers_query_internal_names_resolve",
            "api_resolvers_query_list_user_groups_resolve",
            "api_resolvers_query_vulnerabilities_to_reattack_resolve",
            "api_resolvers_query_groups_with_forces_resolve",
            "front_can_use_groups_searchbar",
            "grant_user_level_role:admin",
            "grant_user_level_role:customer",
            "grant_user_level_role:hacker",
        },
        tags=set(),
    ),
    hacker=dict(
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
# Permission duplication for the old roles
USER_LEVEL_ROLES["analyst"] = USER_LEVEL_ROLES["hacker"]

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
    hacker=dict(
        actions={
            *USER_LEVEL_ROLES["hacker"]["actions"],
            "api_mutations_add_group_mutate",
            "api_mutations_add_organization_mutate",
            "api_resolvers_query_list_user_groups_resolve",
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
            "api_mutations_add_group_mutate",
            "api_mutations_add_organization_mutate",
            "front_can_use_groups_searchbar",
            "keep_default_organization_access",
        },
        tags={
            *USER_LEVEL_ROLES["customer"]["tags"],
        },
    ),
)
# Permission duplication for the old roles
USER_LEVEL_ROLES_FOR_FLUIDATTACKS[
    "analyst"
] = USER_LEVEL_ROLES_FOR_FLUIDATTACKS["hacker"]

# Map(service -> feature)
SERVICE_ATTRIBUTES: Dict[str, Set[str]] = dict(
    continuous={
        "is_continuous",
    },
    service_black={
        "has_service_black",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    },
    service_white={
        "has_service_white",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    },
    forces={
        "has_forces",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    },
    asm={
        "has_asm",
    },
    squad={
        "has_squad",
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
