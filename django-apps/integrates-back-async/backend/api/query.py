# pylint: disable=import-error

from ariadne import QueryType

from backend.api.resolvers import alert, internal_project

QUERY = QueryType()

QUERY.set_field('alert', alert.resolve_alert)
QUERY.set_field('internalProjectNames', internal_project.resolve_project_name)
