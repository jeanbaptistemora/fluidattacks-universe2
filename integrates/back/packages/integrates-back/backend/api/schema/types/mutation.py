# Standard
# None

# Third party
from ariadne import MutationType

# Local
from backend.api.mutations import (
    accept_legal,
    add_event_consult,
    add_environment,
    add_files,
    add_group_consult,
    add_group_tags,
    add_finding_consult,
    add_forces_execution,
    add_git_root,
    add_ip_root,
    add_push_token,
    add_url_root,
    add_stakeholder,
    approve_draft,
    confirm_zero_risk_vuln,
    create_draft,
    create_event,
    create_group,
    create_organization,
    delete_finding,
    delete_vulnerability,
    delete_vulnerability_tags,
    download_event_file,
    download_file,
    download_vulnerability_file,
    edit_group,
    edit_stakeholder,
    edit_stakeholder_organization,
    execute_skims,
    grant_stakeholder_access,
    grant_stakeholder_organization_access,
    handle_vulns_acceptation,
    invalidate_access_token,
    invalidate_cache,
    reject_draft,
    reject_zero_risk_vuln,
    remove_event_evidence,
    remove_finding_evidence,
    remove_files,
    remove_group,
    remove_group_tag,
    remove_stakeholder_access,
    remove_stakeholder_organization_access,
    request_verification_vulnerability,
    request_zero_risk_vuln,
    sign_in,
    solve_event,
    submit_draft,
    subscribe_to_entity_report,
    update_access_token,
    update_environment,
    update_event_evidence,
    update_evidence_description,
    update_evidence,
    update_finding_description,
    update_forces_access_token,
    update_git_environments,
    update_git_root,
    update_organization_policies,
    update_root_cloning_status,
    update_root_state,
    update_severity,
    update_treatment_vulnerability,
    update_vulns_treatment,
    upload_file,
    verify_request_vulnerability
)


MUTATION = MutationType()

MUTATION.set_field('addEventConsult', add_event_consult.mutate)
MUTATION.set_field('addForcesExecution', add_forces_execution.mutate)
MUTATION.set_field('addGitRoot', add_git_root.mutate)
MUTATION.set_field('addIpRoot', add_ip_root.mutate)
MUTATION.set_field('addUrlRoot', add_url_root.mutate)
MUTATION.set_field('addStakeholder', add_stakeholder.mutate)
MUTATION.set_field('approveDraft', approve_draft.mutate)
MUTATION.set_field('confirmZeroRiskVuln', confirm_zero_risk_vuln.mutate)
MUTATION.set_field('createDraft', create_draft.mutate)
MUTATION.set_field('createEvent', create_event.mutate)
MUTATION.set_field('createOrganization', create_organization.mutate)
MUTATION.set_field('deleteFinding', delete_finding.mutate)
MUTATION.set_field('deleteVulnerability', delete_vulnerability.mutate)
MUTATION.set_field('downloadEventFile', download_event_file.mutate)
MUTATION.set_field(
    'editStakeholderOrganization',
    edit_stakeholder_organization.mutate
)
MUTATION.set_field('executeSkims', execute_skims.mutate)
MUTATION.set_field(
    'grantStakeholderOrganizationAccess',
    grant_stakeholder_organization_access.mutate
)
MUTATION.set_field('invalidateCache', invalidate_cache.mutate)
MUTATION.set_field('rejectZeroRiskVuln', reject_zero_risk_vuln.mutate)
MUTATION.set_field('removeEventEvidence', remove_event_evidence.mutate)
MUTATION.set_field(
    'removeStakeholderOrganizationAccess',
    remove_stakeholder_organization_access.mutate
)
MUTATION.set_field('requestZeroRiskVuln', request_zero_risk_vuln.mutate)
MUTATION.set_field('solveEvent', solve_event.mutate)
MUTATION.set_field('submitDraft', submit_draft.mutate)
MUTATION.set_field('updateEventEvidence', update_event_evidence.mutate)
MUTATION.set_field(
    'updateEvidenceDescription',
    update_evidence_description.mutate
)
MUTATION.set_field('updateEvidence', update_evidence.mutate)
MUTATION.set_field(
    'updateForcesAccessToken',
    update_forces_access_token.mutate
)
MUTATION.set_field('updateGitEnvironments', update_git_environments.mutate)
MUTATION.set_field('updateGitRoot', update_git_root.mutate)
MUTATION.set_field(
    'updateOrganizationPolicies',
    update_organization_policies.mutate
)
MUTATION.set_field('updateRootState', update_root_state.mutate)
MUTATION.set_field('updateRootCloningStatus',
                   update_root_cloning_status.mutate)
MUTATION.set_field('updateSeverity', update_severity.mutate)
MUTATION.set_field('uploadFile', upload_file.mutate)

MUTATION.set_field('signIn', sign_in.mutate)
MUTATION.set_field(
    'subscribeToEntityReport',
    subscribe_to_entity_report.mutate
)
MUTATION.set_field('updateAccessToken', update_access_token.mutate)
MUTATION.set_field('invalidateAccessToken', invalidate_access_token.mutate)
MUTATION.set_field('acceptLegal', accept_legal.mutate)
MUTATION.set_field('addPushToken', add_push_token.mutate)
MUTATION.set_field('grantStakeholderAccess', grant_stakeholder_access.mutate)
MUTATION.set_field('removeStakeholderAccess', remove_stakeholder_access.mutate)
MUTATION.set_field('editStakeholder', edit_stakeholder.mutate)
MUTATION.set_field('addEnvironments', add_environment.mutate)
MUTATION.set_field('addFiles', add_files.mutate)
MUTATION.set_field('downloadFile', download_file.mutate)
MUTATION.set_field('removeFiles', remove_files.mutate)
MUTATION.set_field('updateEnvironment', update_environment.mutate)
MUTATION.set_field('createProject', create_group.mutate)
MUTATION.set_field('editGroup', edit_group.mutate)
MUTATION.set_field('removeGroup', remove_group.mutate)
MUTATION.set_field('addProjectConsult', add_group_consult.mutate)
MUTATION.set_field('addTags', add_group_tags.mutate)
MUTATION.set_field('removeTag', remove_group_tag.mutate)
MUTATION.set_field('removeEvidence', remove_finding_evidence.mutate)
MUTATION.set_field('addFindingConsult', add_finding_consult.mutate)
MUTATION.set_field('updateDescription', update_finding_description.mutate)
MUTATION.set_field('rejectDraft', reject_draft.mutate)
MUTATION.set_field('deleteTags', delete_vulnerability_tags.mutate)
MUTATION.set_field(
    'updateTreatmentVuln',
    update_treatment_vulnerability.mutate
)
MUTATION.set_field(
    'requestVerificationVuln',
    request_verification_vulnerability.mutate
)
MUTATION.set_field('verifyRequestVuln', verify_request_vulnerability.mutate)
MUTATION.set_field('downloadVulnFile', download_vulnerability_file.mutate)
MUTATION.set_field('handleVulnsAcceptation', handle_vulns_acceptation.mutate)
MUTATION.set_field('updateVulnsTreatment', update_vulns_treatment.mutate)
