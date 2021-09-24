# None


from api.mutations import (
    accept_legal,
    acknowledge_concurrent_session,
    activate_root,
    add_draft,
    add_draft_new,
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
    approve_draft_new,
    confirm_vulnerabilities_zero_risk,
    deactivate_organization_finding_policy,
    deactivate_root,
    download_event_file,
    download_file,
    download_vulnerability_file,
    grant_stakeholder_access,
    grant_stakeholder_organization_access,
    handle_organization_finding_policy_acceptation,
    handle_vulnerabilities_acceptation,
    handle_vulnerabilities_acceptation_new,
    invalidate_access_token,
    invalidate_cache,
    reject_draft,
    reject_draft_new,
    reject_vulnerabilities_zero_risk,
    reject_vulnerabilities_zero_risk_new,
    remove_event_evidence,
    remove_files,
    remove_finding,
    remove_finding_evidence,
    remove_finding_evidence_new,
    remove_finding_new,
    remove_group,
    remove_group_new,
    remove_group_tag,
    remove_stakeholder_access,
    remove_stakeholder_organization_access,
    remove_vulnerability,
    remove_vulnerability_new,
    remove_vulnerability_tags,
    request_vulnerabilities_verification,
    request_vulnerabilities_verification_new,
    request_vulnerabilities_zero_risk,
    request_vulnerabilities_zero_risk_new,
    sign_in,
    sign_post_url,
    solve_event,
    submit_draft,
    submit_draft_new,
    submit_machine_job,
    submit_organization_finding_policy,
    subscribe_to_entity_report,
    unsubscribe_from_group,
    update_access_token,
    update_event_evidence,
    update_evidence,
    update_evidence_description,
    update_evidence_description_new,
    update_evidence_new,
    update_finding_description,
    update_finding_description_new,
    update_forces_access_token,
    update_git_environments,
    update_git_root,
    update_group,
    update_group_stakeholder,
    update_organization_policies,
    update_organization_stakeholder,
    update_root_cloning_status,
    update_severity,
    update_severity_new,
    update_toe_lines_sorts,
    update_vulnerabilities_treatment,
    update_vulnerabilities_treatment_new,
    update_vulnerability_commit,
    update_vulnerability_commit_new,
    update_vulnerability_treatment,
    upload_file,
    upload_file_new,
    verify_vulnerabilities_request,
    verify_vulnerabilities_request_new,
)
from ariadne import (
    MutationType,
)
from context import (
    FI_API_STATUS,
)

MUTATION = MutationType()
MUTATION.set_field("acceptLegal", accept_legal.mutate)
MUTATION.set_field(
    "acknowledgeConcurrentSession", acknowledge_concurrent_session.mutate
)
MUTATION.set_field("activateRoot", activate_root.mutate)
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
MUTATION.set_field("grantStakeholderAccess", grant_stakeholder_access.mutate)
MUTATION.set_field(
    "grantStakeholderOrganizationAccess",
    grant_stakeholder_organization_access.mutate,
)
MUTATION.set_field(
    "handleOrganizationFindingPolicyAcceptation",
    handle_organization_finding_policy_acceptation.mutate,
)
MUTATION.set_field("invalidateAccessToken", invalidate_access_token.mutate)
MUTATION.set_field("invalidateCache", invalidate_cache.mutate)
MUTATION.set_field("removeEventEvidence", remove_event_evidence.mutate)
MUTATION.set_field("removeStakeholderAccess", remove_stakeholder_access.mutate)
MUTATION.set_field(
    "removeStakeholderOrganizationAccess",
    remove_stakeholder_organization_access.mutate,
)
MUTATION.set_field("removeFiles", remove_files.mutate)
MUTATION.set_field("removeGroupTag", remove_group_tag.mutate)
MUTATION.set_field("removeTags", remove_vulnerability_tags.mutate)
MUTATION.set_field("signIn", sign_in.mutate)
MUTATION.set_field("signPostUrl", sign_post_url.mutate)
MUTATION.set_field("solveEvent", solve_event.mutate)
MUTATION.set_field(
    "submitOrganizationFindingPolicy",
    submit_organization_finding_policy.mutate,
)
MUTATION.set_field(
    "subscribeToEntityReport", subscribe_to_entity_report.mutate
)
MUTATION.set_field("unsubscribeFromGroup", unsubscribe_from_group.mutate)
MUTATION.set_field("updateAccessToken", update_access_token.mutate)
MUTATION.set_field("updateEventEvidence", update_event_evidence.mutate)
MUTATION.set_field(
    "updateForcesAccessToken", update_forces_access_token.mutate
)
MUTATION.set_field("updateGitEnvironments", update_git_environments.mutate)
MUTATION.set_field("updateGitRoot", update_git_root.mutate)
MUTATION.set_field("updateGroup", update_group.mutate)
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
MUTATION.set_field("updateToeLinesSorts", update_toe_lines_sorts.mutate)
MUTATION.set_field(
    "updateVulnerabilityTreatment", update_vulnerability_treatment.mutate
)

if FI_API_STATUS == "migration":
    MUTATION.set_field("addDraft", add_draft_new.mutate)
    MUTATION.set_field("approveDraft", approve_draft_new.mutate)
    MUTATION.set_field(
        "downloadVulnerabilityFile", download_vulnerability_file.mutate
    )
    MUTATION.set_field(
        "handleVulnerabilitiesAcceptation",
        handle_vulnerabilities_acceptation_new.mutate,
    )
    MUTATION.set_field("rejectDraft", reject_draft_new.mutate)
    MUTATION.set_field(
        "rejectVulnerabilitiesZeroRisk",
        reject_vulnerabilities_zero_risk_new.mutate,
    )
    MUTATION.set_field("removeFinding", remove_finding_new.mutate)
    MUTATION.set_field("removeVulnerability", remove_vulnerability_new.mutate)
    MUTATION.set_field("removeEvidence", remove_finding_evidence_new.mutate)
    MUTATION.set_field("removeGroup", remove_group_new.mutate)
    MUTATION.set_field(
        "requestVulnerabilitiesVerification",
        request_vulnerabilities_verification_new.mutate,
    )
    MUTATION.set_field(
        "requestVulnerabilitiesZeroRisk",
        request_vulnerabilities_zero_risk_new.mutate,
    )
    MUTATION.set_field("submitDraft", submit_draft_new.mutate)
    MUTATION.set_field("submitMachineJob", submit_machine_job.mutate)
    MUTATION.set_field(
        "updateDescription", update_finding_description_new.mutate
    )
    MUTATION.set_field("updateEvidence", update_evidence_new.mutate)
    MUTATION.set_field(
        "updateEvidenceDescription", update_evidence_description_new.mutate
    )
    MUTATION.set_field("updateSeverity", update_severity_new.mutate)
    MUTATION.set_field(
        "updateVulnerabilityCommit", update_vulnerability_commit_new.mutate
    )
    MUTATION.set_field(
        "updateVulnerabilitiesTreatment",
        update_vulnerabilities_treatment_new.mutate,
    )
    MUTATION.set_field("uploadFile", upload_file_new.mutate)
    MUTATION.set_field(
        "verifyVulnerabilitiesRequest",
        verify_vulnerabilities_request_new.mutate,
    )
    # -----------------------Deprecated mutations------------------------------
    MUTATION.set_field(
        "verifyRequestVuln", verify_vulnerabilities_request_new.mutate
    )
    # -------------------------------------------------------------------------
else:
    MUTATION.set_field("addDraft", add_draft.mutate)
    MUTATION.set_field("approveDraft", approve_draft.mutate)
    MUTATION.set_field(
        "downloadVulnerabilityFile", download_vulnerability_file.mutate
    )
    MUTATION.set_field(
        "handleVulnerabilitiesAcceptation",
        handle_vulnerabilities_acceptation.mutate,
    )
    MUTATION.set_field("rejectDraft", reject_draft.mutate)
    MUTATION.set_field(
        "rejectVulnerabilitiesZeroRisk",
        reject_vulnerabilities_zero_risk.mutate,
    )
    MUTATION.set_field("removeEvidence", remove_finding_evidence.mutate)
    MUTATION.set_field("removeFinding", remove_finding.mutate)
    MUTATION.set_field("removeGroup", remove_group.mutate)
    MUTATION.set_field("removeVulnerability", remove_vulnerability.mutate)
    MUTATION.set_field(
        "requestVulnerabilitiesVerification",
        request_vulnerabilities_verification.mutate,
    )
    MUTATION.set_field(
        "requestVulnerabilitiesZeroRisk",
        request_vulnerabilities_zero_risk.mutate,
    )
    MUTATION.set_field("submitDraft", submit_draft.mutate)
    MUTATION.set_field("submitMachineJob", submit_machine_job.mutate)
    MUTATION.set_field("updateDescription", update_finding_description.mutate)
    MUTATION.set_field("updateEvidence", update_evidence.mutate)
    MUTATION.set_field(
        "updateEvidenceDescription", update_evidence_description.mutate
    )
    MUTATION.set_field("updateSeverity", update_severity.mutate)
    MUTATION.set_field(
        "updateVulnerabilityCommit", update_vulnerability_commit.mutate
    )
    MUTATION.set_field(
        "updateVulnerabilitiesTreatment",
        update_vulnerabilities_treatment.mutate,
    )
    MUTATION.set_field("uploadFile", upload_file.mutate)
    MUTATION.set_field(
        "verifyVulnerabilitiesRequest", verify_vulnerabilities_request.mutate
    )
    # -----------------------Deprecated mutations------------------------------
    MUTATION.set_field(
        "verifyRequestVuln", verify_vulnerabilities_request.mutate
    )
