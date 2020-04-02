# pylint: disable=import-error

from backend.api.resolvers import (
    alert, cache, event, finding, me, user, resource, project,
    vulnerability
)

from ariadne import MutationType

MUTATION = MutationType()

MUTATION.set_field('setAlert', alert.resolve_set_alert)
MUTATION.set_field('invalidateCache', cache.resolve_invalidate_cache)
MUTATION.set_field('updateEvent', event.resolve_update_event)
MUTATION.set_field('createEvent', event.resolve_create_event)
MUTATION.set_field('solveEvent', event.resolve_solve_event)
MUTATION.set_field('addEventComment', event.resolve_add_event_comment)
MUTATION.set_field('updateEventEvidence', event.resolve_update_event_evidence)
MUTATION.set_field('downloadEventFile', event.resolve_download_event_file)
MUTATION.set_field('removeEventEvidence', event.resolve_remove_event_evidence)
MUTATION.set_field('signIn', me.resolve_sign_in)
MUTATION.set_field('updateAccessToken', me.resolve_update_access_token)
MUTATION.set_field('invalidateAccessToken', me.resolve_invalidate_access_token)
MUTATION.set_field('acceptLegal', me.resolve_accept_legal)
MUTATION.set_field('addUser', user.resolve_add_user)
MUTATION.set_field('grantUserAccess', user.resolve_grant_user_access)
MUTATION.set_field('removeUserAccess', user.resolve_remove_user_access)
MUTATION.set_field('editUser', user.resolve_edit_user)
MUTATION.set_field('addRepositories', resource.resolve_add_repositories)
MUTATION.set_field('addEnvironments', resource.resolve_add_environments)
MUTATION.set_field('addFiles', resource.resolve_add_files)
MUTATION.set_field('downloadFile', resource.resolve_download_file)
MUTATION.set_field('removeFiles', resource.resolve_remove_files)
MUTATION.set_field('updateRepository', resource.resolve_update_repository)
MUTATION.set_field('updateEnvironment', resource.resolve_update_environment)
MUTATION.set_field('createProject', project.resolve_create_project)
MUTATION.set_field('requestRemoveProject',
                   project.resolve_request_remove_project)
MUTATION.set_field('rejectRemoveProject',
                   project.resolve_reject_remove_project)
MUTATION.set_field('addTags', project.resolve_add_tags)
MUTATION.set_field('removeTag', project.resolve_remove_tag)
MUTATION.set_field('addAllProjectAccess',
                   project.resolve_add_all_project_access)
MUTATION.set_field('removeAllProjectAccess',
                   project.resolve_remove_all_project_access)
MUTATION.set_field('removeEvidence', finding.resolve_finding_mutation)
MUTATION.set_field('updateEvidence', finding.resolve_finding_mutation)
MUTATION.set_field('updateEvidenceDescription',
                   finding.resolve_update_evidence_description)
MUTATION.set_field('updateSeverity',
                   finding.resolve_finding_mutation)
MUTATION.set_field('updateDescription',
                   finding.resolve_finding_mutation)
MUTATION.set_field('updateClientDescription',
                   finding.resolve_finding_mutation)
MUTATION.set_field('verifyFinding', finding.resolve_verify_finding)
MUTATION.set_field('handleAcceptation', finding.resolve_handle_acceptation)
MUTATION.set_field('rejectDraft', finding.resolve_reject_draft)
MUTATION.set_field('deleteFinding', finding.resolve_delete_finding)
MUTATION.set_field('approveDraft', finding.resolve_approve_draft)
MUTATION.set_field('createDraft', finding.resolve_create_draft)
MUTATION.set_field('submitDraft', finding.resolve_submit_draft)
MUTATION.set_field('approveVulnerability',
                   vulnerability.resolve_approve_vulnerability)
MUTATION.set_field('deleteTags', vulnerability.resolve_delete_tags)
MUTATION.set_field('updateTreatmentVuln',
                   vulnerability.resolve_update_treatment_vuln)
MUTATION.set_field('requestVerificationVuln',
                   vulnerability.resolve_request_verification_vuln)
MUTATION.set_field('verifyRequestVuln',
                   vulnerability.resolve_verify_request_vuln)
MUTATION.set_field('deleteVulnerability',
                   vulnerability.resolve_delete_vulnerability)
MUTATION.set_field('uploadFile',
                   vulnerability.resolve_upload_file)
