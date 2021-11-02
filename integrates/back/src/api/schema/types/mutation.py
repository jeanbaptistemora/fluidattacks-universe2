# None


from api.mutations import (
    accept_legal,
    acknowledge_concurrent_session,
    activate_root,
    add_draft,
    add_event,
    add_event_consult,
    add_files_to_db,
    add_finding_consult,
    add_forces_execution,
    add_git_root,
    add_group,
    add_group_consult,
    add_group_tags,
    add_ip_root,
    add_organization,
    add_organization_finding_policy,
    add_push_token,
    add_stakeholder,
    add_url_root,
    approve_draft,
    confirm_vulnerabilities_zero_risk,
    deactivate_organization_finding_policy,
    deactivate_root,
    download_event_file,
    download_file,
    download_vulnerability_file,
    grant_stakeholder_access,
    grant_stakeholder_organization_access,
    handle_organization_finding_policy_acceptance,
    handle_vulnerabilities_acceptance,
    invalidate_access_token,
    invalidate_cache,
    move_root,
    reject_draft,
    reject_vulnerabilities_zero_risk,
    remove_event_evidence,
    remove_files,
    remove_finding,
    remove_finding_evidence,
    remove_group,
    remove_group_tag,
    remove_stakeholder,
    remove_stakeholder_access,
    remove_stakeholder_organization_access,
    remove_vulnerability,
    remove_vulnerability_tags,
    request_vulnerabilities_verification,
    request_vulnerabilities_zero_risk,
    sign_in,
    sign_post_url,
    sign_post_url_requester,
    solve_event,
    submit_draft,
    submit_machine_job,
    submit_organization_finding_policy,
    subscribe_to_entity_report,
    unsubscribe_from_group,
    update_access_token,
    update_event_evidence,
    update_evidence,
    update_evidence_description,
    update_finding_description,
    update_forces_access_token,
    update_git_environments,
    update_git_root,
    update_group,
    update_group_info,
    update_group_stakeholder,
    update_organization_policies,
    update_organization_stakeholder,
    update_root_cloning_status,
    update_severity,
    update_toe_lines_sorts,
    update_vulnerabilities_treatment,
    update_vulnerability_commit,
    update_vulnerability_treatment,
    upload_file,
    verify_vulnerabilities_request,
    virus_scan_file,
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
MUTATION.set_field("addDraft", add_draft.mutate)
MUTATION.set_field("addEvent", add_event.mutate)
MUTATION.set_field("addEventConsult", add_event_consult.mutate)
MUTATION.set_field("addFilesToDb", add_files_to_db.mutate)
MUTATION.set_field("addFindingConsult", add_finding_consult.mutate)
MUTATION.set_field("addForcesExecution", add_forces_execution.mutate)
MUTATION.set_field("addGitRoot", add_git_root.mutate)
MUTATION.set_field("addGroup", add_group.mutate)
MUTATION.set_field("addGroupConsult", add_group_consult.mutate)
MUTATION.set_field("addGroupTags", add_group_tags.mutate)
MUTATION.set_field("addIpRoot", add_ip_root.mutate)
MUTATION.set_field("addOrganization", add_organization.mutate)
MUTATION.set_field(
    "addOrganizationFindingPolicy", add_organization_finding_policy.mutate
)
MUTATION.set_field("addPushToken", add_push_token.mutate)
MUTATION.set_field("addStakeholder", add_stakeholder.mutate)
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
MUTATION.set_field("downloadEventFile", download_event_file.mutate)
MUTATION.set_field("downloadFile", download_file.mutate)
MUTATION.set_field(
    "downloadVulnerabilityFile", download_vulnerability_file.mutate
)
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
MUTATION.set_field("invalidateCache", invalidate_cache.mutate)
MUTATION.set_field("moveRoot", move_root.mutate)
MUTATION.set_field("rejectDraft", reject_draft.mutate)
MUTATION.set_field(
    "rejectVulnerabilitiesZeroRisk",
    reject_vulnerabilities_zero_risk.mutate,
)
MUTATION.set_field("removeEventEvidence", remove_event_evidence.mutate)
MUTATION.set_field("removeEvidence", remove_finding_evidence.mutate)
MUTATION.set_field("removeFinding", remove_finding.mutate)
MUTATION.set_field("removeStakeholder", remove_stakeholder.mutate)
MUTATION.set_field("removeStakeholderAccess", remove_stakeholder_access.mutate)
MUTATION.set_field(
    "removeStakeholderOrganizationAccess",
    remove_stakeholder_organization_access.mutate,
)
MUTATION.set_field("removeFiles", remove_files.mutate)
MUTATION.set_field("removeGroup", remove_group.mutate)
MUTATION.set_field("removeGroupTag", remove_group_tag.mutate)
MUTATION.set_field("removeTags", remove_vulnerability_tags.mutate)
MUTATION.set_field("removeVulnerability", remove_vulnerability.mutate)
MUTATION.set_field(
    "requestVulnerabilitiesVerification",
    request_vulnerabilities_verification.mutate,
)
MUTATION.set_field(
    "requestVulnerabilitiesZeroRisk",
    request_vulnerabilities_zero_risk.mutate,
)
MUTATION.set_field("signIn", sign_in.mutate)
MUTATION.set_field("signPostUrl", sign_post_url.mutate)
MUTATION.set_field("signPostUrlRequester", sign_post_url_requester.mutate)
MUTATION.set_field("solveEvent", solve_event.mutate)
MUTATION.set_field("submitDraft", submit_draft.mutate)
MUTATION.set_field("submitMachineJob", submit_machine_job.mutate)
MUTATION.set_field(
    "submitOrganizationFindingPolicy",
    submit_organization_finding_policy.mutate,
)
MUTATION.set_field(
    "subscribeToEntityReport", subscribe_to_entity_report.mutate
)
MUTATION.set_field("unsubscribeFromGroup", unsubscribe_from_group.mutate)
MUTATION.set_field("updateAccessToken", update_access_token.mutate)
MUTATION.set_field("updateDescription", update_finding_description.mutate)
MUTATION.set_field("updateEventEvidence", update_event_evidence.mutate)
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
MUTATION.set_field("updateGroupInfo", update_group_info.mutate)
MUTATION.set_field("updateGroupStakeholder", update_group_stakeholder.mutate)
MUTATION.set_field(
    "updateOrganizationPolicies", update_organization_policies.mutate
)
MUTATION.set_field(
    "updateOrganizationStakeholder", update_organization_stakeholder.mutate
)
MUTATION.set_field(
    "updateRootCloningStatus", update_root_cloning_status.mutate
)
MUTATION.set_field("updateSeverity", update_severity.mutate)
MUTATION.set_field("updateToeLinesSorts", update_toe_lines_sorts.mutate)
MUTATION.set_field(
    "updateVulnerabilityCommit", update_vulnerability_commit.mutate
)
MUTATION.set_field(
    "updateVulnerabilitiesTreatment",
    update_vulnerabilities_treatment.mutate,
)
MUTATION.set_field(
    "updateVulnerabilityTreatment", update_vulnerability_treatment.mutate
)
MUTATION.set_field("uploadFile", upload_file.mutate)
MUTATION.set_field(
    "verifyVulnerabilitiesRequest",
    verify_vulnerabilities_request.mutate,
)
MUTATION.set_field("virusScanFile", virus_scan_file.mutate)
