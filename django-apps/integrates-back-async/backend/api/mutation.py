# pylint: disable=import-error

from ariadne import MutationType

from backend.api.resolvers import alert, cache

MUTATION = MutationType()

MUTATION.set_field('setAlert', alert.resolve_set_alert)
MUTATION.set_field('invalidateCache', cache.resolve_invalidate_cache)
