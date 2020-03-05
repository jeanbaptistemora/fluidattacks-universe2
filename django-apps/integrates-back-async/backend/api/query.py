# pylint: disable=import-error

from ariadne import QueryType

from backend.api.resolvers import alert

QUERY = QueryType()

QUERY.set_field('alert', alert.resolve_alert)
