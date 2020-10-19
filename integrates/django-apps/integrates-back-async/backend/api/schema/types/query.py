# Standard
# None

# Third party
from ariadne import QueryType

# Local
from backend.api.resolvers import (
    finding,
    vulnerability
)
from backend.api.resolvers.new.query import (
    event,
    events,
    forces_execution,
    forces_executions,
    forces_executions_new,
    group,
    groups,
    internal_names,
    me,
    organization,
    organization_id,
    report,
    resources,
    stakeholder,
    tag,
    user_list_groups
)


QUERY = QueryType()

# Query resolvers
QUERY.set_field('event', event.resolve)
QUERY.set_field('events', events.resolve)
QUERY.set_field('finding', finding.resolve_finding)
QUERY.set_field('forcesExecution', forces_execution.resolve)
QUERY.set_field('forcesExecutions', forces_executions.resolve)
QUERY.set_field('forcesExecutionsNew', forces_executions_new.resolve)
QUERY.set_field('internalNames', internal_names.resolve)
QUERY.set_field('me', me.resolve)
QUERY.set_field('organization', organization.resolve)
QUERY.set_field('organizationId', organization_id.resolve)
QUERY.set_field('project', group.resolve)
QUERY.set_field('projects', groups.resolve)
QUERY.set_field('report', report.resolve)
QUERY.set_field('resources', resources.resolve)
QUERY.set_field('stakeholder', stakeholder.resolve)
QUERY.set_field('tag', tag.resolve)
QUERY.set_field('userListProjects', user_list_groups.resolve)
QUERY.set_field('vulnerability', vulnerability.resolve_vulnerability)
