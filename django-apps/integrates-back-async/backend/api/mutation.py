# pylint: disable=import-error

from backend.api.resolvers import alert, cache, event, me

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
