# pylint: disable=import-error

from backend.api.resolvers import (
    alert, cache, event, finding, me, user, report, resource, project,
    subscription, vulnerability
)

from ariadne import MutationType

MUTATION = MutationType()

MUTATION.set_field('setAlert', alert.resolve_set_alert)
MUTATION.set_field('invalidateCache', cache.resolve_invalidate_cache)
MUTATION.set_field('createEvent', event.resolve_event_mutation)
MUTATION.set_field('solveEvent', event.resolve_event_mutation)
MUTATION.set_field('addEventComment', event.resolve_event_mutation)
MUTATION.set_field('updateEventEvidence', event.resolve_event_mutation)
MUTATION.set_field('downloadEventFile', event.resolve_event_mutation)
MUTATION.set_field('removeEventEvidence', event.resolve_event_mutation)
MUTATION.set_field('signIn', me.resolve_me_mutation)
MUTATION.set_field('updateAccessToken', me.resolve_me_mutation)
MUTATION.set_field('invalidateAccessToken', me.resolve_me_mutation)
MUTATION.set_field('acceptLegal', me.resolve_me_mutation)
MUTATION.set_field('addUser', user.resolve_user_mutation)
MUTATION.set_field('grantUserAccess', user.resolve_user_mutation)
MUTATION.set_field('removeUserAccess', user.resolve_user_mutation)
MUTATION.set_field('editUser', user.resolve_user_mutation)
MUTATION.set_field('addRepositories', resource.resolve_resources_mutation)
MUTATION.set_field('addEnvironments', resource.resolve_resources_mutation)
MUTATION.set_field('addFiles', resource.resolve_resources_mutation)
MUTATION.set_field('downloadFile', resource.resolve_resources_mutation)
MUTATION.set_field('removeFiles', resource.resolve_resources_mutation)
MUTATION.set_field('updateRepository', resource.resolve_resources_mutation)
MUTATION.set_field('updateEnvironment', resource.resolve_resources_mutation)
MUTATION.set_field('createProject', project.resolve_project_mutation)
MUTATION.set_field('requestRemoveProject',
                   project.resolve_project_mutation)
MUTATION.set_field('rejectRemoveProject',
                   project.resolve_project_mutation)
MUTATION.set_field('addProjectComment',
                   project.resolve_project_mutation)
MUTATION.set_field('addTags', project.resolve_project_mutation)
MUTATION.set_field('removeTag', project.resolve_project_mutation)
MUTATION.set_field('addAllProjectAccess',
                   project.resolve_project_mutation)
MUTATION.set_field('removeAllProjectAccess',
                   project.resolve_project_mutation)
MUTATION.set_field('removeEvidence', finding.resolve_finding_mutation)
MUTATION.set_field('updateEvidence', finding.resolve_finding_mutation)
MUTATION.set_field('updateEvidenceDescription',
                   finding.resolve_finding_mutation)
MUTATION.set_field('updateSeverity',
                   finding.resolve_finding_mutation)
MUTATION.set_field('addFindingComment',
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
MUTATION.set_field('approveVulnerability',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('deleteTags', vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('updateTreatmentVuln',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('requestVerificationVuln',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('verifyRequestVuln',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('deleteVulnerability',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('uploadFile',
                   vulnerability.resolve_vulnerability_mutation)
MUTATION.set_field('postBroadcastMessage',
                   subscription.resolve_subscription_mutation)
MUTATION.set_field('requestProjectReport',
                   report.resolve_report_mutation)
