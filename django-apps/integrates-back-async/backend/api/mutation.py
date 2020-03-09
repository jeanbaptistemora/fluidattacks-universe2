# pylint: disable=import-error

from ariadne import MutationType

from backend.api.resolvers import alert, cache, event

MUTATION = MutationType()

MUTATION.set_field('setAlert', alert.resolve_set_alert)
MUTATION.set_field('invalidateCache', cache.resolve_invalidate_cache)
MUTATION.set_field('updateEvent', event.resolve_update_event)
MUTATION.set_field('createEvent', event.resolve_create_event)
MUTATION.set_field('solveEvent', event.resolve_solve_event)
