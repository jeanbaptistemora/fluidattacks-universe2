from api.resolvers.organization import (
    analytics,
    billing,
    compliance,
    covered_authors,
    covered_commits,
    covered_repositories,
    credentials,
    finding_policies,
    groups,
    inactivity_period,
    integration_repositories,
    integration_repositories_connection,
    max_acceptance_days,
    max_acceptance_severity,
    max_number_acceptances,
    min_acceptance_severity,
    min_breaking_severity,
    missed_authors,
    missed_commits,
    missed_repositories,
    organization_id,
    permissions,
    stakeholders,
    trial,
    user_role,
    vulnerabilities_url,
    vulnerability_grace_period,
)
from ariadne import (
    ObjectType,
)

ORGANIZATION: ObjectType = ObjectType("Organization")
ORGANIZATION.set_field("analytics", analytics.resolve)
ORGANIZATION.set_field("billing", billing.resolve)
ORGANIZATION.set_field("compliance", compliance.resolve)
ORGANIZATION.set_field("coveredAuthors", covered_authors.resolve)
ORGANIZATION.set_field("coveredCommits", covered_commits.resolve)
ORGANIZATION.set_field("coveredRepositories", covered_repositories.resolve)
ORGANIZATION.set_field("credentials", credentials.resolve)
ORGANIZATION.set_field("findingPolicies", finding_policies.resolve)
ORGANIZATION.set_field("groups", groups.resolve)
ORGANIZATION.set_field("id", organization_id.resolve)
ORGANIZATION.set_field("inactivityPeriod", inactivity_period.resolve)
ORGANIZATION.set_field(
    "integrationRepositories", integration_repositories.resolve
)
ORGANIZATION.set_field(
    "integrationRepositoriesConnection",
    integration_repositories_connection.resolve,
)
ORGANIZATION.set_field("maxAcceptanceDays", max_acceptance_days.resolve)
ORGANIZATION.set_field(
    "maxAcceptanceSeverity", max_acceptance_severity.resolve
)
ORGANIZATION.set_field("missedAuthors", missed_authors.resolve)
ORGANIZATION.set_field("missedCommits", missed_commits.resolve)
ORGANIZATION.set_field("missedRepositories", missed_repositories.resolve)
ORGANIZATION.set_field(
    "minAcceptanceSeverity", min_acceptance_severity.resolve
)
ORGANIZATION.set_field("maxNumberAcceptances", max_number_acceptances.resolve)
ORGANIZATION.set_field("minBreakingSeverity", min_breaking_severity.resolve)
ORGANIZATION.set_field("permissions", permissions.resolve)
ORGANIZATION.set_field("stakeholders", stakeholders.resolve)
ORGANIZATION.set_field("trial", trial.resolve)
ORGANIZATION.set_field("userRole", user_role.resolve)
ORGANIZATION.set_field("vulnerabilitiesUrl", vulnerabilities_url.resolve)
ORGANIZATION.set_field(
    "vulnerabilityGracePeriod", vulnerability_grace_period.resolve
)
