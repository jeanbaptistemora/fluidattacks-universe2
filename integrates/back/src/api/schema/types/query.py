# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.query import (
    billing,
    enrollment,
    environment_url,
    event,
    events,
    finding,
    forces_execution,
    forces_executions,
    group,
    groups_with_forces,
    list_user_groups,
    me,
    organization,
    organization_id,
    report,
    resources,
    root,
    stakeholder,
    tag,
    vulnerabilities_to_reattack,
    vulnerability,
)
from ariadne import (
    QueryType,
)

QUERY = QueryType()
QUERY.set_field("billing", billing.resolve)
QUERY.set_field("enrollment", enrollment.resolve)
QUERY.set_field("event", event.resolve)
QUERY.set_field("events", events.resolve)
QUERY.set_field("finding", finding.resolve)
QUERY.set_field("forcesExecution", forces_execution.resolve)
QUERY.set_field("forcesExecutions", forces_executions.resolve)
QUERY.set_field("group", group.resolve)
QUERY.set_field("groupsWithForces", groups_with_forces.resolve)
QUERY.set_field("listUserGroups", list_user_groups.resolve)
QUERY.set_field("me", me.resolve)
QUERY.set_field("organization", organization.resolve)
QUERY.set_field("organizationId", organization_id.resolve)
QUERY.set_field("report", report.resolve)
QUERY.set_field("resources", resources.resolve)
QUERY.set_field("root", root.resolve)
QUERY.set_field("stakeholder", stakeholder.resolve)
QUERY.set_field("tag", tag.resolve)
QUERY.set_field("vulnerability", vulnerability.resolve)
QUERY.set_field(
    "vulnerabilitiesToReattack", vulnerabilities_to_reattack.resolve
)
QUERY.set_field("environmentUrl", environment_url.resolve)
