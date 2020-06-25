from backend.api.resolvers import (
    analytics,
    alert,
    event,
    finding,
    forces,
    internal_project,
    me,
    organization,
    project,
    resource,
    tag,
    user
)

from ariadne import QueryType

QUERY = QueryType()

# Query resolvers
QUERY.set_field('alert', alert.resolve_alert)
QUERY.set_field('analytics', analytics.resolve)
QUERY.set_field('internalProjectNames', internal_project.resolve_project_name)
QUERY.set_field('event', event.resolve_event)
QUERY.set_field('events', event.resolve_events)
QUERY.set_field('me', me.resolve_me)
QUERY.set_field('resources', resource.resolve_resources)
QUERY.set_field('user', user.resolve_user)
QUERY.set_field('forcesExecutions', forces.resolve_forces_executions)
QUERY.set_field('finding', finding.resolve_finding)
QUERY.set_field('organization', organization.resolve_organization)
QUERY.set_field('project', project.resolve_project)
QUERY.set_field('aliveProjects', project.resolve_alive_projects)
QUERY.set_field('projects', project.resolve_alive_projects)
QUERY.set_field('userListProjects', user.resolve_user_list_projects)
QUERY.set_field('tag', tag.resolve_tag)
