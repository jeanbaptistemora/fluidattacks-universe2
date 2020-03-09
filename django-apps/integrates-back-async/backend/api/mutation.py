# pylint: disable=import-error

from backend.api.resolvers import alert, cache, event

from ariadne import MutationType

MUTATION = MutationType()

MUTATION.set_field('setAlert', alert.resolve_set_alert)
MUTATION.set_field('invalidateCache', cache.resolve_invalidate_cache)
MUTATION.set_field('updateEvent', event.resolve_update_event)
MUTATION.set_field('createEvent', event.resolve_create_event)
MUTATION.set_field('solveEvent', event.resolve_solve_event)
MUTATION.set_field('addEventComment', event.resolve_add_event_comment)
MUTATION.set_field('updateEventEvidence', event.resolve_update_event_evidence)
