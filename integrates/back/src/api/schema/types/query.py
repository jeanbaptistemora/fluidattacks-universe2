# None


from api.resolvers.query import (
    event,
    events,
    finding,
    finding_new,
    forces_execution,
    forces_executions,
    group,
    groups_with_forces,
    internal_names,
    me,
    organization,
    organization_id,
    report,
    resources,
    stakeholder,
    tag,
    user_list_groups,
    vulnerability,
    vulnerability_new,
    vulns_to_reattack,
)
from ariadne import (
    QueryType,
)
from context import (
    FI_API_STATUS,
)

QUERY = QueryType()
QUERY.set_field("event", event.resolve)
QUERY.set_field("events", events.resolve)
QUERY.set_field("forcesExecution", forces_execution.resolve)
QUERY.set_field("forcesExecutions", forces_executions.resolve)
QUERY.set_field("groupsWithForces", groups_with_forces.resolve)
QUERY.set_field("internalNames", internal_names.resolve)
QUERY.set_field("me", me.resolve)
QUERY.set_field("organization", organization.resolve)
QUERY.set_field("organizationId", organization_id.resolve)
QUERY.set_field("project", group.resolve)
QUERY.set_field("report", report.resolve)
QUERY.set_field("resources", resources.resolve)
QUERY.set_field("stakeholder", stakeholder.resolve)
QUERY.set_field("tag", tag.resolve)
QUERY.set_field("userListProjects", user_list_groups.resolve)
QUERY.set_field("vulnsToReattack", vulns_to_reattack.resolve)

# Standardization Fields
QUERY.set_field("group", group.resolve)
QUERY.set_field("userListGroups", user_list_groups.resolve)

if FI_API_STATUS == "migration":
    QUERY.set_field("finding", finding_new.resolve)
    QUERY.set_field("vulnerability", vulnerability_new.resolve)
else:
    QUERY.set_field("finding", finding.resolve)
    QUERY.set_field("vulnerability", vulnerability.resolve)
