# pylint: disable=import-error

from ariadne import MutationType

from backend.api.resolvers import cache

MUTATION = MutationType()

MUTATION.set_field('invalidateCache', cache.resolve_invalidate_cache)
