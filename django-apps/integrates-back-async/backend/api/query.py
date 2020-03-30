# pylint: disable=import-error

from backend.api.resolvers import (
    alert, finding, internal_project, event,
    forces, me, project, resource, user
)

from ariadne import QueryType, ObjectType

ME = ObjectType('Me')
FINDING = ObjectType('Finding')
QUERY = QueryType()

# Query resolvers
QUERY.set_field('alert', alert.resolve_alert)
QUERY.set_field('internalProjectNames', internal_project.resolve_project_name)
QUERY.set_field('event', event.resolve_event)
QUERY.set_field('events', event.resolve_events)
QUERY.set_field('me', me.resolve_me)
QUERY.set_field('resources', resource.resolve_resources)
QUERY.set_field('user', user.resolve_user)
QUERY.set_field('forcesExecutions', forces.resolve_forces_executions)
QUERY.set_field('finding', finding.resolve_finding)
QUERY.set_field('project', project.resolve_project)

# Specific field resolvers
ME.set_field('role', me.resolve_role)
FINDING.set_field('vulnerabilities', finding.resolve_vulnerabilities)
