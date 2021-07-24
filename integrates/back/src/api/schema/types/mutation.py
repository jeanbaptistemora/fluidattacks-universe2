# None


from api.mutations import (
    accept_legal,
    acknowledge_concurrent_session,
    activate_root,
    add_draft,
    add_draft_new,
    add_event,
    add_event_consult,
    add_files,
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
    confirm_zero_risk_vulnerabilities,
    deactivate_organization_finding_policy,
    deactivate_root,
    download_event_file,
    download_file,
    download_vulnerability_file,
    edit_group,
    edit_stakeholder,
    edit_stakeholder_organization,
    grant_stakeholder_access,
    grant_stakeholder_organization_access,
    handle_organization_finding_policy_acceptation,
    handle_vulnerabilities_acceptation,
    invalidate_access_token,
    invalidate_cache,
    reject_draft,
    reject_draft_new,
    reject_zero_risk_vulnerabilities,
    reject_zero_risk_vulnerabilities_new,
    remove_event_evidence,
    remove_files,
    remove_finding,
    remove_finding_evidence,
    remove_finding_evidence_new,
    remove_finding_new,
    remove_group,
    remove_group_tag,
    remove_stakeholder_access,
    remove_stakeholder_organization_access,
    remove_vulnerability,
    remove_vulnerability_new,
    remove_vulnerability_tags,
    request_verification_vulnerabilities,
    request_verification_vulnerabilities_new,
    request_zero_risk_vuln_new,
    request_zero_risk_vulnerabilities,
    sign_in,
    solve_event,
    submit_draft,
    submit_draft_new,
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
    update_organization_policies,
    update_root_cloning_status,
    update_root_state,
    update_severity,
    update_severity_new,
    update_toe_lines_sorts,
    update_vulnerabilities_treatment,
    update_vulnerability_commit,
    update_vulnerability_treatment,
    upload_file,
    upload_file_new,
    verify_request_vulnerabilities,
    verify_request_vulnerabilities_new,
)
from ariadne import (
    MutationType,
)
from context import (
    FI_API_STATUS,
)

MUTATION = MutationType()
MUTATION.set_field("activateRoot", activate_root.mutate)
MUTATION.set_field("addEventConsult", add_event_consult.mutate)
MUTATION.set_field("addForcesExecution", add_forces_execution.mutate)
MUTATION.set_field("addGitRoot", add_git_root.mutate)
MUTATION.set_field("addIpRoot", add_ip_root.mutate)
MUTATION.set_field(
    "addOrgFindingPolicy", add_organization_finding_policy.mutate
)
MUTATION.set_field(
    "addOrganizationFindingPolicy", add_organization_finding_policy.mutate
)
MUTATION.set_field("addUrlRoot", add_url_root.mutate)
MUTATION.set_field("addStakeholder", add_stakeholder.mutate)
MUTATION.set_field(
    "confirmZeroRiskVuln", confirm_zero_risk_vulnerabilities.mutate
)
MUTATION.set_field("createEvent", add_event.mutate)
MUTATION.set_field("createOrganization", add_organization.mutate)
MUTATION.set_field(
    "deactivateOrgFindingPolicy", deactivate_organization_finding_policy.mutate
)
MUTATION.set_field(
    "deactivateOrganizationFindingPolicy",
    deactivate_organization_finding_policy.mutate,
)
MUTATION.set_field("deactivateRoot", deactivate_root.mutate)
MUTATION.set_field("downloadEventFile", download_event_file.mutate)
MUTATION.set_field(
    "editStakeholderOrganization", edit_stakeholder_organization.mutate
)
MUTATION.set_field(
    "grantStakeholderOrganizationAccess",
    grant_stakeholder_organization_access.mutate,
)
MUTATION.set_field(
    "handleOrgFindingPolicyAcceptation",
    handle_organization_finding_policy_acceptation.mutate,
)
MUTATION.set_field(
    "handleOrganizationFindingPolicyAcceptation",
    handle_organization_finding_policy_acceptation.mutate,
)
MUTATION.set_field("invalidateCache", invalidate_cache.mutate)
MUTATION.set_field("removeEventEvidence", remove_event_evidence.mutate)
MUTATION.set_field(
    "removeStakeholderOrganizationAccess",
    remove_stakeholder_organization_access.mutate,
)
MUTATION.set_field("solveEvent", solve_event.mutate)
MUTATION.set_field(
    "submitOrganizationFindingPolicy",
    submit_organization_finding_policy.mutate,
)
MUTATION.set_field("updateEventEvidence", update_event_evidence.mutate)

MUTATION.set_field(
    "updateForcesAccessToken", update_forces_access_token.mutate
)
MUTATION.set_field("updateGitEnvironments", update_git_environments.mutate)
MUTATION.set_field("updateGitRoot", update_git_root.mutate)
MUTATION.set_field(
    "updateOrganizationPolicies", update_organization_policies.mutate
)
MUTATION.set_field("updateRootState", update_root_state.mutate)
MUTATION.set_field(
    "updateRootCloningStatus", update_root_cloning_status.mutate
)

MUTATION.set_field("signIn", sign_in.mutate)
MUTATION.set_field(
    "subscribeToEntityReport", subscribe_to_entity_report.mutate
)
MUTATION.set_field("updateAccessToken", update_access_token.mutate)
MUTATION.set_field("invalidateAccessToken", invalidate_access_token.mutate)
MUTATION.set_field("acceptLegal", accept_legal.mutate)
MUTATION.set_field(
    "acknowledgeConcurrentSession", acknowledge_concurrent_session.mutate
)
MUTATION.set_field("addPushToken", add_push_token.mutate)
MUTATION.set_field("grantStakeholderAccess", grant_stakeholder_access.mutate)
MUTATION.set_field("removeStakeholderAccess", remove_stakeholder_access.mutate)
MUTATION.set_field("editStakeholder", edit_stakeholder.mutate)
MUTATION.set_field("addFiles", add_files.mutate)
MUTATION.set_field("downloadFile", download_file.mutate)
MUTATION.set_field("removeFiles", remove_files.mutate)
MUTATION.set_field("createProject", add_group.mutate)
MUTATION.set_field("editGroup", edit_group.mutate)
MUTATION.set_field("removeGroup", remove_group.mutate)
MUTATION.set_field("addProjectConsult", add_group_consult.mutate)
MUTATION.set_field("addTags", add_group_tags.mutate)
MUTATION.set_field("removeTag", remove_group_tag.mutate)
MUTATION.set_field("addFindingConsult", add_finding_consult.mutate)
MUTATION.set_field("unsubscribeFromGroup", unsubscribe_from_group.mutate)
MUTATION.set_field("deleteTags", remove_vulnerability_tags.mutate)
MUTATION.set_field(
    "updateTreatmentVuln", update_vulnerability_treatment.mutate
)
MUTATION.set_field(
    "updateVulnerabilityTreatment", update_vulnerability_treatment.mutate
)
MUTATION.set_field("downloadVulnFile", download_vulnerability_file.mutate)
MUTATION.set_field(
    "handleVulnsAcceptation", handle_vulnerabilities_acceptation.mutate
)
MUTATION.set_field("updateVulnCommit", update_vulnerability_commit.mutate)
MUTATION.set_field(
    "updateVulnerabilityCommit", update_vulnerability_commit.mutate
)
MUTATION.set_field(
    "updateVulnsTreatment", update_vulnerabilities_treatment.mutate
)
MUTATION.set_field(
    "updateVulnerabilitiesTreatment", update_vulnerabilities_treatment.mutate
)
MUTATION.set_field("updateToeLinesSorts", update_toe_lines_sorts.mutate)

# Standardization Fields
MUTATION.set_field("addEvent", add_event.mutate)
MUTATION.set_field("addGroup", add_group.mutate)
MUTATION.set_field("addGroupConsult", add_group_consult.mutate)
MUTATION.set_field("addOrganization", add_organization.mutate)
MUTATION.set_field("createGroup", add_group.mutate)
MUTATION.set_field(
    "confirmZeroRiskVulnerabilities", confirm_zero_risk_vulnerabilities.mutate
)
MUTATION.set_field("removeTags", remove_vulnerability_tags.mutate)
MUTATION.set_field(
    "downloadVulnerabilityFile", download_vulnerability_file.mutate
)
MUTATION.set_field(
    "handleVulnerabilitiesAcceptation",
    handle_vulnerabilities_acceptation.mutate,
)


if FI_API_STATUS == "migration":
    MUTATION.set_field("addDraft", add_draft_new.mutate)
    MUTATION.set_field("approveDraft", approve_draft_new.mutate)
    MUTATION.set_field("createDraft", add_draft_new.mutate)
    MUTATION.set_field("deleteFinding", remove_finding_new.mutate)
    MUTATION.set_field("removeFinding", remove_finding_new.mutate)
    MUTATION.set_field("deleteVulnerability", remove_vulnerability_new.mutate)
    MUTATION.set_field("removeVulnerability", remove_vulnerability_new.mutate)
    MUTATION.set_field("rejectDraft", reject_draft_new.mutate)
    MUTATION.set_field(
        "rejectZeroRiskVuln", reject_zero_risk_vulnerabilities_new.mutate
    )
    MUTATION.set_field(
        "rejectZeroRiskVulnerabilities",
        reject_zero_risk_vulnerabilities_new.mutate,
    )
    MUTATION.set_field("removeEvidence", remove_finding_evidence_new.mutate)
    MUTATION.set_field(
        "requestVerificationVuln",
        request_verification_vulnerabilities_new.mutate,
    )
    MUTATION.set_field(
        "requestVerificationVulnerabilities",
        request_verification_vulnerabilities_new.mutate,
    )
    MUTATION.set_field(
        "requestZeroRiskVuln", request_zero_risk_vuln_new.mutate
    )
    MUTATION.set_field(
        "requestZeroRiskVulnerabilities", request_zero_risk_vuln_new.mutate
    )
    MUTATION.set_field("submitDraft", submit_draft_new.mutate)
    MUTATION.set_field(
        "updateDescription", update_finding_description_new.mutate
    )
    MUTATION.set_field("updateEvidence", update_evidence_new.mutate)
    MUTATION.set_field(
        "updateEvidenceDescription", update_evidence_description_new.mutate
    )
    MUTATION.set_field("updateSeverity", update_severity_new.mutate)
    MUTATION.set_field("uploadFile", upload_file_new.mutate)
    MUTATION.set_field(
        "verifyRequestVuln", verify_request_vulnerabilities_new.mutate
    )
    MUTATION.set_field(
        "verifyRequestVulnerabilities",
        verify_request_vulnerabilities_new.mutate,
    )
else:
    MUTATION.set_field("addDraft", add_draft.mutate)
    MUTATION.set_field("approveDraft", approve_draft.mutate)
    MUTATION.set_field("createDraft", add_draft.mutate)
    MUTATION.set_field("deleteFinding", remove_finding.mutate)
    MUTATION.set_field("removeFinding", remove_finding.mutate)
    MUTATION.set_field("deleteVulnerability", remove_vulnerability.mutate)
    MUTATION.set_field("removeVulnerability", remove_vulnerability.mutate)
    MUTATION.set_field("rejectDraft", reject_draft.mutate)
    MUTATION.set_field(
        "rejectZeroRiskVuln", reject_zero_risk_vulnerabilities.mutate
    )
    MUTATION.set_field(
        "rejectZeroRiskVulnerabilities",
        reject_zero_risk_vulnerabilities.mutate,
    )
    MUTATION.set_field("removeEvidence", remove_finding_evidence.mutate)
    MUTATION.set_field(
        "requestVerificationVuln", request_verification_vulnerabilities.mutate
    )
    MUTATION.set_field(
        "requestVerificationVulnerabilities",
        request_verification_vulnerabilities.mutate,
    )
    MUTATION.set_field(
        "requestZeroRiskVuln", request_zero_risk_vulnerabilities.mutate
    )
    MUTATION.set_field(
        "requestZeroRiskVulnerabilities",
        request_zero_risk_vulnerabilities.mutate,
    )
    MUTATION.set_field("submitDraft", submit_draft.mutate)
    MUTATION.set_field("updateDescription", update_finding_description.mutate)
    MUTATION.set_field("updateEvidence", update_evidence.mutate)
    MUTATION.set_field(
        "updateEvidenceDescription", update_evidence_description.mutate
    )
    MUTATION.set_field("updateSeverity", update_severity.mutate)
    MUTATION.set_field("uploadFile", upload_file.mutate)
    MUTATION.set_field(
        "verifyRequestVuln", verify_request_vulnerabilities.mutate
    )
    MUTATION.set_field(
        "verifyRequestVulnerabilities", verify_request_vulnerabilities.mutate
    )
