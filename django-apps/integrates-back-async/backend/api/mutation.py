# pylint: disable=import-error

from backend.api.resolvers import alert, cache, event, me, user, resource

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
