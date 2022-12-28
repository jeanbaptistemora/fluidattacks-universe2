from api.mutations import (
    accept_legal,
    acknowledge_concurrent_session,
    activate_root,
    add_credentials,
    add_draft,
    add_enrollment,
    add_event,
    add_event_consult,
    add_files_to_db,
    add_finding_consult,
    add_forces_execution,
    add_git_environment,
    add_git_environment_secret,
    add_git_root,
    add_group,
    add_group_consult,
    add_group_tags,
    add_ip_root,
    add_machine_execution,
    add_organization,
    add_organization_finding_policy,
    add_payment_method,
    add_secret,
    add_stakeholder,
    add_toe_input,
    add_toe_lines,
    add_toe_port,
    add_url_root,
    approve_draft,
    confirm_vulnerabilities_zero_risk,
    deactivate_organization_finding_policy,
    deactivate_root,
    download_billing_file,
    download_event_file,
    download_file,
    download_vulnerability_file,
    finish_machine_execution,
    grant_stakeholder_access,
    grant_stakeholder_organization_access,
    handle_organization_finding_policy_acceptance,
    handle_vulnerabilities_acceptance,
    invalidate_access_token,
    move_root,
    refresh_toe_lines,
    reject_draft,
    reject_event_solution,
    reject_vulnerabilities_zero_risk,
    remove_credentials,
    remove_environment_url,
    remove_environment_url_secret,
    remove_event_evidence,
    remove_files,
    remove_finding,
    remove_finding_evidence,
    remove_group,
    remove_group_tag,
    remove_payment_method,
    remove_secret,
    remove_stakeholder,
    remove_stakeholder_access,
    remove_stakeholder_organization_access,
    remove_vulnerability,
    remove_vulnerability_tags,
    request_event_verification,
    request_groups_upgrade,
    request_vulnerabilities_hold,
    request_vulnerabilities_verification,
    request_vulnerabilities_zero_risk,
    send_assigned_notification,
    send_sales_mail_to_get_squad_plan,
    send_vulnerability_notification,
    sign_post_url,
    solve_event,
    start_machine_execution,
    submit_draft,
    submit_group_machine_execution,
    submit_machine_job,
    submit_organization_finding_policy,
    subscribe_to_entity_report,
    sync_git_root,
    unsubscribe_from_group,
    update_access_token,
    update_credentials,
    update_event,
    update_event_evidence,
    update_event_solving_reason,
    update_evidence,
    update_evidence_description,
    update_finding_description,
    update_forces_access_token,
    update_git_environments,
    update_git_root,
    update_group,
    update_group_access_info,
    update_group_disambiguation,
    update_group_info,
    update_group_managed,
    update_group_payment_id,
    update_group_policies,
    update_group_stakeholder,
    update_ip_root,
    update_notifications_preferences,
    update_organization_policies,
    update_organization_stakeholder,
    update_payment_method,
    update_root_cloning_status,
    update_severity,
    update_stakeholder_phone,
    update_subscription,
    update_toe_input,
    update_toe_lines_attacked_lines,
    update_toe_lines_sorts,
    update_toe_port,
    update_tours,
    update_url_root,
    update_vulnerabilities_treatment,
    update_vulnerability_description,
    update_vulnerability_treatment,
    upload_file,
    validate_git_access,
    verify_stakeholder,
    verify_vulnerabilities_request,
)
from ariadne import (
    MutationType,
)

MUTATION = MutationType()
MUTATION.set_field("acceptLegal", accept_legal.mutate)
MUTATION.set_field(
    "acknowledgeConcurrentSession", acknowledge_concurrent_session.mutate
)
MUTATION.set_field("activateRoot", activate_root.mutate)
MUTATION.set_field("addCredentials", add_credentials.mutate)
MUTATION.set_field("addDraft", add_draft.mutate)
MUTATION.set_field("addEnrollment", add_enrollment.mutate)
MUTATION.set_field("addEvent", add_event.mutate)
MUTATION.set_field("addEventConsult", add_event_consult.mutate)
MUTATION.set_field("addFilesToDb", add_files_to_db.mutate)
MUTATION.set_field("addFindingConsult", add_finding_consult.mutate)
MUTATION.set_field("addForcesExecution", add_forces_execution.mutate)
MUTATION.set_field("addGitRoot", add_git_root.mutate)
MUTATION.set_field("addMachineExecution", add_machine_execution.mutate)
MUTATION.set_field("addSecret", add_secret.mutate)
MUTATION.set_field(
    "addGitEnvironmentSecret", add_git_environment_secret.mutate
)
MUTATION.set_field("addGitEnvironmentUrl", add_git_environment.mutate)
MUTATION.set_field("addGroup", add_group.mutate)
MUTATION.set_field("addGroupConsult", add_group_consult.mutate)
MUTATION.set_field("addGroupTags", add_group_tags.mutate)
MUTATION.set_field("addIpRoot", add_ip_root.mutate)
MUTATION.set_field("addOrganization", add_organization.mutate)
MUTATION.set_field(
    "addOrganizationFindingPolicy", add_organization_finding_policy.mutate
)
MUTATION.set_field("addPaymentMethod", add_payment_method.mutate)
MUTATION.set_field("addStakeholder", add_stakeholder.mutate)
MUTATION.set_field("addToeInput", add_toe_input.mutate)
MUTATION.set_field("addToeLines", add_toe_lines.mutate)
MUTATION.set_field("addToePort", add_toe_port.mutate)
MUTATION.set_field("addUrlRoot", add_url_root.mutate)
MUTATION.set_field("approveDraft", approve_draft.mutate)
MUTATION.set_field(
    "confirmVulnerabilitiesZeroRisk", confirm_vulnerabilities_zero_risk.mutate
)
MUTATION.set_field(
    "deactivateOrganizationFindingPolicy",
    deactivate_organization_finding_policy.mutate,
)
MUTATION.set_field("deactivateRoot", deactivate_root.mutate)
MUTATION.set_field("downloadBillingFile", download_billing_file.mutate)
MUTATION.set_field("downloadEventFile", download_event_file.mutate)
MUTATION.set_field("downloadFile", download_file.mutate)
MUTATION.set_field(
    "downloadVulnerabilityFile", download_vulnerability_file.mutate
)
MUTATION.set_field("finishMachineExecution", finish_machine_execution.mutate)
MUTATION.set_field("startMachineExecution", start_machine_execution.mutate)
MUTATION.set_field("grantStakeholderAccess", grant_stakeholder_access.mutate)
MUTATION.set_field(
    "grantStakeholderOrganizationAccess",
    grant_stakeholder_organization_access.mutate,
)
MUTATION.set_field(
    "handleOrganizationFindingPolicyAcceptance",
    handle_organization_finding_policy_acceptance.mutate,
)
MUTATION.set_field(
    "handleVulnerabilitiesAcceptance",
    handle_vulnerabilities_acceptance.mutate,
)
MUTATION.set_field("invalidateAccessToken", invalidate_access_token.mutate)
MUTATION.set_field("moveRoot", move_root.mutate)
MUTATION.set_field("refreshToeLines", refresh_toe_lines.mutate)
MUTATION.set_field("rejectDraft", reject_draft.mutate)
MUTATION.set_field("rejectEventSolution", reject_event_solution.mutate)
MUTATION.set_field(
    "rejectVulnerabilitiesZeroRisk",
    reject_vulnerabilities_zero_risk.mutate,
)
MUTATION.set_field("removeCredentials", remove_credentials.mutate)
MUTATION.set_field("removeEventEvidence", remove_event_evidence.mutate)
MUTATION.set_field("removeEvidence", remove_finding_evidence.mutate)
MUTATION.set_field("removeFinding", remove_finding.mutate)
MUTATION.set_field("removeSecret", remove_secret.mutate)
MUTATION.set_field(
    "removeEnvironmentUrlSecret", remove_environment_url_secret.mutate
)
MUTATION.set_field("removeEnvironmentUrl", remove_environment_url.mutate)
MUTATION.set_field("removeStakeholder", remove_stakeholder.mutate)
MUTATION.set_field("removeStakeholderAccess", remove_stakeholder_access.mutate)
MUTATION.set_field(
    "removeStakeholderOrganizationAccess",
    remove_stakeholder_organization_access.mutate,
)
MUTATION.set_field("removeFiles", remove_files.mutate)
MUTATION.set_field("removeGroup", remove_group.mutate)
MUTATION.set_field("removeGroupTag", remove_group_tag.mutate)
MUTATION.set_field("removePaymentMethod", remove_payment_method.mutate)
MUTATION.set_field("removeTags", remove_vulnerability_tags.mutate)
MUTATION.set_field("removeVulnerability", remove_vulnerability.mutate)
MUTATION.set_field(
    "requestEventVerification", request_event_verification.mutate
)
MUTATION.set_field(
    "requestVulnerabilitiesHold", request_vulnerabilities_hold.mutate
)
MUTATION.set_field(
    "requestVulnerabilitiesVerification",
    request_vulnerabilities_verification.mutate,
)
MUTATION.set_field(
    "requestVulnerabilitiesZeroRisk",
    request_vulnerabilities_zero_risk.mutate,
)
MUTATION.set_field(
    "sendAssignedNotification", send_assigned_notification.mutate
)
MUTATION.set_field(
    "sendSalesMailToGetSquadPlan",
    send_sales_mail_to_get_squad_plan.mutate,
)
MUTATION.set_field(
    "sendVulnerabilityNotification", send_vulnerability_notification.mutate
)
MUTATION.set_field("signPostUrl", sign_post_url.mutate)
MUTATION.set_field("solveEvent", solve_event.mutate)
MUTATION.set_field("submitDraft", submit_draft.mutate)
MUTATION.set_field(
    "submitGroupMachineExecution", submit_group_machine_execution.mutate
)
MUTATION.set_field("submitMachineJob", submit_machine_job.mutate)
MUTATION.set_field(
    "submitOrganizationFindingPolicy",
    submit_organization_finding_policy.mutate,
)
MUTATION.set_field(
    "subscribeToEntityReport", subscribe_to_entity_report.mutate
)
MUTATION.set_field("syncGitRoot", sync_git_root.mutate)
MUTATION.set_field("unsubscribeFromGroup", unsubscribe_from_group.mutate)
MUTATION.set_field("updateAccessToken", update_access_token.mutate)
MUTATION.set_field("updateCredentials", update_credentials.mutate)
MUTATION.set_field("updateDescription", update_finding_description.mutate)
MUTATION.set_field("updateEvent", update_event.mutate)
MUTATION.set_field("updateEventEvidence", update_event_evidence.mutate)
MUTATION.set_field(
    "updateEventSolvingReason", update_event_solving_reason.mutate
)
MUTATION.set_field("updateEvidence", update_evidence.mutate)
MUTATION.set_field(
    "updateEvidenceDescription", update_evidence_description.mutate
)
MUTATION.set_field(
    "updateForcesAccessToken", update_forces_access_token.mutate
)
MUTATION.set_field("updateGitEnvironments", update_git_environments.mutate)
MUTATION.set_field("updateGitRoot", update_git_root.mutate)
MUTATION.set_field("updateGroup", update_group.mutate)
MUTATION.set_field("updateGroupAccessInfo", update_group_access_info.mutate)
MUTATION.set_field(
    "updateGroupDisambiguation", update_group_disambiguation.mutate
)
MUTATION.set_field("updateGroupInfo", update_group_info.mutate)
MUTATION.set_field("updateGroupManaged", update_group_managed.mutate)
MUTATION.set_field("updateGroupPaymentId", update_group_payment_id.mutate)
MUTATION.set_field("updateGroupPolicies", update_group_policies.mutate)
MUTATION.set_field("updateGroupStakeholder", update_group_stakeholder.mutate)
MUTATION.set_field("updateIpRoot", update_ip_root.mutate)
MUTATION.set_field(
    "updateNotificationsPreferences", update_notifications_preferences.mutate
)
MUTATION.set_field(
    "updateOrganizationPolicies", update_organization_policies.mutate
)
MUTATION.set_field(
    "updateOrganizationStakeholder", update_organization_stakeholder.mutate
)
MUTATION.set_field("updatePaymentMethod", update_payment_method.mutate)
MUTATION.set_field(
    "updateRootCloningStatus", update_root_cloning_status.mutate
)
MUTATION.set_field("updateSeverity", update_severity.mutate)
MUTATION.set_field("updateStakeholderPhone", update_stakeholder_phone.mutate)
MUTATION.set_field("updateSubscription", update_subscription.mutate)
MUTATION.set_field("updateToeInput", update_toe_input.mutate)
MUTATION.set_field(
    "updateToeLinesAttackedLines", update_toe_lines_attacked_lines.mutate
)
MUTATION.set_field("updateToeLinesSorts", update_toe_lines_sorts.mutate)
MUTATION.set_field("updateToePort", update_toe_port.mutate)
MUTATION.set_field("updateTours", update_tours.mutate)
MUTATION.set_field("updateUrlRoot", update_url_root.mutate)
MUTATION.set_field(
    "updateVulnerabilityDescription", update_vulnerability_description.mutate
)
MUTATION.set_field(
    "updateVulnerabilitiesTreatment",
    update_vulnerabilities_treatment.mutate,
)
MUTATION.set_field(
    "updateVulnerabilityTreatment", update_vulnerability_treatment.mutate
)
MUTATION.set_field("uploadFile", upload_file.mutate)
MUTATION.set_field("requestGroupsUpgrade", request_groups_upgrade.mutate)
MUTATION.set_field("validateGitAccess", validate_git_access.mutate)
MUTATION.set_field("verifyStakeholder", verify_stakeholder.mutate)
MUTATION.set_field(
    "verifyVulnerabilitiesRequest",
    verify_vulnerabilities_request.mutate,
)
