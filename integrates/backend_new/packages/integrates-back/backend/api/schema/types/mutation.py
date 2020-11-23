# Standard
# None

# Third party
from ariadne import MutationType

# Local
from backend.api.mutations import (
    add_event_consult,
    add_forces_execution,
    add_git_root,
    add_ip_root,
    add_url_root,
    add_stakeholder,
    approve_draft,
    confirm_zero_risk_vuln,
    create_draft,
    create_event,
    create_organization,
    delete_finding,
    delete_vulnerability,
    download_event_file,
    edit_stakeholder_organization,
    execute_skims,
    grant_stakeholder_organization_access,
    handle_vulns_acceptation,
    invalidate_cache,
    reject_zero_risk_vuln,
    remove_event_evidence,
    remove_group,
    remove_stakeholder_organization_access,
    request_zero_risk_vuln,
    solve_event,
    submit_draft,
    update_event_evidence,
    update_evidence_description,
    update_evidence,
    update_forces_access_token,
    update_organization_policies,
    update_severity,
    upload_file
)
from backend.api.resolvers import (
    finding,
    me,
    project,
    resource,
    user,
    vulnerability
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
MUTATION.set_field(
    'updateOrganizationPolicies',
    update_organization_policies.mutate
)
MUTATION.set_field('updateSeverity', update_severity.mutate)
MUTATION.set_field('uploadFile', upload_file.mutate)

MUTATION.set_field('signIn', me.resolve_me_mutation)
MUTATION.set_field('subscribeToEntityReport', me.resolve_me_mutation)
MUTATION.set_field('updateAccessToken', me.resolve_me_mutation)
MUTATION.set_field('invalidateAccessToken', me.resolve_me_mutation)
MUTATION.set_field('acceptLegal', me.resolve_me_mutation)
MUTATION.set_field('addPushToken', me.resolve_me_mutation)
MUTATION.set_field('grantStakeholderAccess', user.resolve_user_mutation)
MUTATION.set_field('removeStakeholderAccess', user.resolve_user_mutation)
MUTATION.set_field('editStakeholder', user.resolve_user_mutation)
MUTATION.set_field('addRepositories', resource.resolve_resources_mutation)
MUTATION.set_field('addEnvironments', resource.resolve_resources_mutation)
MUTATION.set_field('addFiles', resource.resolve_resources_mutation)
MUTATION.set_field('downloadFile', resource.resolve_resources_mutation)
MUTATION.set_field('removeFiles', resource.resolve_resources_mutation)
MUTATION.set_field('updateRepository', resource.resolve_resources_mutation)
MUTATION.set_field('updateEnvironment', resource.resolve_resources_mutation)
MUTATION.set_field('createProject', project.resolve_project_mutation)
MUTATION.set_field('editGroup', project.resolve_project_mutation)
MUTATION.set_field('removeGroup', remove_group.mutate)
MUTATION.set_field('rejectRemoveProject',
                   project.resolve_project_mutation)
MUTATION.set_field('addProjectConsult',
                   project.resolve_project_mutation)
MUTATION.set_field('addTags', project.resolve_project_mutation)
MUTATION.set_field('removeTag', project.resolve_project_mutation)
MUTATION.set_field('removeEvidence', finding.resolve_finding_mutation)
MUTATION.set_field('addFindingConsult',
                   finding.resolve_finding_mutation)
MUTATION.set_field('updateDescription',
                   finding.resolve_finding_mutation)
MUTATION.set_field('updateClientDescription',
                   finding.resolve_finding_mutation)
MUTATION.set_field('handleAcceptation', finding.resolve_finding_mutation)
MUTATION.set_field('rejectDraft', finding.resolve_finding_mutation)
MUTATION.set_field('deleteTags', vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('updateTreatmentVuln',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('requestVerificationVuln',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('verifyRequestVuln',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('downloadVulnFile',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('handleVulnsAcceptation', handle_vulns_acceptation.mutate)
