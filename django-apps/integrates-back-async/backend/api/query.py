# pylint: disable=import-error

from backend.api.resolvers import (
    alert, finding, internal_project, event, forces, me, resource, user
)

from ariadne import QueryType, ObjectType

ME = ObjectType('Me')
QUERY = QueryType()

QUERY.set_field('alert', alert.resolve_alert)
QUERY.set_field('internalProjectNames', internal_project.resolve_project_name)
QUERY.set_field('event', event.resolve_event)
QUERY.set_field('events', event.resolve_events)
QUERY.set_field('me', me.resolve_me)
QUERY.set_field('resources', resource.resolve_resources)
QUERY.set_field('user', user.resolve_user)
QUERY.set_field('forcesExecutions', forces.resolve_forces_executions)
QUERY.set_field('finding', finding.resolve_finding)
ME.set_field('role', me.resolve_role)
