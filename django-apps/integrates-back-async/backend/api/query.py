# pylint: disable=import-error

from backend.api.resolvers import (
    alert, internal_project, event, me, user
)

from ariadne import QueryType

QUERY = QueryType()

QUERY.set_field('alert', alert.resolve_alert)
QUERY.set_field('internalProjectNames', internal_project.resolve_project_name)
QUERY.set_field('event', event.resolve_event)
QUERY.set_field('events', event.resolve_events)
QUERY.set_field('me', me.resolve_me)
QUERY.set_field('user', user.resolve_user)
