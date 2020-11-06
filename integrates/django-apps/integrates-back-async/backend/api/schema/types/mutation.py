# Standard
# None

# Third party
from ariadne import MutationType

# Local
from backend.api.mutations import (
    add_event_consult,
    add_forces_execution,
    confirm_zero_risk_vuln,
    create_event,
    create_organization,
    delete_vulnerability,
    download_event_file,
    edit_stakeholder_organization,
    execute_skims,
    grant_stakeholder_organization_access,
    invalidate_cache,
    request_zero_risk_vuln,
    remove_event_evidence,
    solve_event,
    update_event_evidence,
    update_evidence,
    update_forces_access_token
)
from backend.api.resolvers import (
    finding,
    me,
    organization,
    project,
    resource,
    user,
    vulnerability
)


MUTATION = MutationType()

MUTATION.set_field('addEventConsult', add_event_consult.mutate)
MUTATION.set_field('addForcesExecution', add_forces_execution.mutate)
MUTATION.set_field('confirmZeroRiskVuln', confirm_zero_risk_vuln.mutate)
MUTATION.set_field('createEvent', create_event.mutate)
MUTATION.set_field('createOrganization', create_organization.mutate)
MUTATION.set_field('deleteVulnerability', delete_vulnerability.mutate)
MUTATION.set_field('downloadEventFile', download_event_file.mutate)
MUTATION.set_field(
    'editStakeholderOrganization',
    edit_stakeholder_organization.mutate
)
MUTATION.set_field(
    'grantStakeholderOrganizationAccess',
    grant_stakeholder_organization_access.mutate
)
MUTATION.set_field('invalidateCache', invalidate_cache.mutate)
MUTATION.set_field('removeEventEvidence', remove_event_evidence.mutate)
MUTATION.set_field('requestZeroRiskVuln', request_zero_risk_vuln.mutate)
MUTATION.set_field('solveEvent', solve_event.mutate)
MUTATION.set_field('updateEventEvidence', update_event_evidence.mutate)
MUTATION.set_field('updateEvidence', update_evidence.mutate)
MUTATION.set_field(
    'updateForcesAccessToken',
    update_forces_access_token.mutate
)

MUTATION.set_field('signIn', me.resolve_me_mutation)
MUTATION.set_field('subscribeToEntityReport', me.resolve_me_mutation)
MUTATION.set_field('updateAccessToken', me.resolve_me_mutation)
MUTATION.set_field('invalidateAccessToken', me.resolve_me_mutation)
MUTATION.set_field('acceptLegal', me.resolve_me_mutation)
MUTATION.set_field('addPushToken', me.resolve_me_mutation)
MUTATION.set_field('addStakeholder', user.resolve_user_mutation)
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
MUTATION.set_field(
    'removeStakeholderOrganizationAccess',
    organization.resolve_organization_mutation
)
MUTATION.set_field(
    'updateOrganizationPolicies', organization.resolve_organization_mutation
)
MUTATION.set_field('createProject', project.resolve_project_mutation)
MUTATION.set_field('editGroup', project.resolve_project_mutation)
MUTATION.set_field('rejectRemoveProject',
                   project.resolve_project_mutation)
MUTATION.set_field('addProjectConsult',
                   project.resolve_project_mutation)
MUTATION.set_field('addTags', project.resolve_project_mutation)
MUTATION.set_field('removeTag', project.resolve_project_mutation)
MUTATION.set_field('removeEvidence', finding.resolve_finding_mutation)
MUTATION.set_field('updateEvidenceDescription',
                   finding.resolve_finding_mutation)
MUTATION.set_field('updateSeverity',
                   finding.resolve_finding_mutation)
MUTATION.set_field('addFindingConsult',
                   finding.resolve_finding_mutation)
MUTATION.set_field('updateDescription',
                   finding.resolve_finding_mutation)
MUTATION.set_field('updateClientDescription',
                   finding.resolve_finding_mutation)
MUTATION.set_field('handleAcceptation', finding.resolve_finding_mutation)
MUTATION.set_field('rejectDraft', finding.resolve_finding_mutation)
MUTATION.set_field('deleteFinding', finding.resolve_finding_mutation)
MUTATION.set_field('approveDraft', finding.resolve_finding_mutation)
MUTATION.set_field('createDraft', finding.resolve_finding_mutation)
MUTATION.set_field('submitDraft', finding.resolve_finding_mutation)
MUTATION.set_field('deleteTags', vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('updateTreatmentVuln',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('requestVerificationVuln',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('verifyRequestVuln',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('uploadFile',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('downloadVulnFile',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('executeSkims', execute_skims.mutate)
