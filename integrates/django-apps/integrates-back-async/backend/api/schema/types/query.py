# Standard
# None

# Third party
from ariadne import QueryType

# Local
from backend.api.resolvers import (
    event,
    finding,
    forces,
    internal_names,
    me,
    project,
    report,
    resource,
    tag,
    user,
    vulnerability
)
from backend.api.resolvers.new.query import (
    groups,
    organization,
    organization_id,
)


QUERY = QueryType()

# Query resolvers
QUERY.set_field('internalNames', internal_names.resolve_project_name)
QUERY.set_field('event', event.resolve_event)
QUERY.set_field('events', event.resolve_events)
QUERY.set_field('me', me.resolve_me)
QUERY.set_field('resources', resource.resolve_resources)
QUERY.set_field('stakeholder', user.resolve_user)
QUERY.set_field('forcesExecution', forces.resolve_forces_execution)
QUERY.set_field('forcesExecutions', forces.resolve_forces_executions)
QUERY.set_field('forcesExecutionsNew', forces.resolve_forces_executions_new)
QUERY.set_field('finding', finding.resolve_finding)
QUERY.set_field('vulnerability', vulnerability.resolve_vulnerability)
QUERY.set_field('organization', organization.resolve)
QUERY.set_field('organizationId', organization_id.resolve)
QUERY.set_field('project', project.resolve_project)
QUERY.set_field('projects', groups.resolve)
QUERY.set_field('userListProjects', user.resolve_user_list_projects)
QUERY.set_field('tag', tag.resolve_tag)
QUERY.set_field('report', report.resolve_report)
