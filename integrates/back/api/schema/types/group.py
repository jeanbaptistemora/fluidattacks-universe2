# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.group import (
    analytics,
    bill,
    consulting,
    drafts,
    events,
    findings,
    last_closing_vuln_finding,
    max_open_severity_finding,
    max_severity_finding,
    max_severity,
    organization,
    service_attributes,
    stakeholders,
    total_findings,
    total_treatment,
    user_role
)


GROUP: ObjectType = ObjectType('Project')

GROUP.set_field('analytics', analytics.resolve)
GROUP.set_field('bill', bill.resolve)
GROUP.set_field('consulting', consulting.resolve)
GROUP.set_field('drafts', drafts.resolve)
GROUP.set_field('events', events.resolve)
GROUP.set_field('findings', findings.resolve)
GROUP.set_field('lastClosingVulnFinding', last_closing_vuln_finding.resolve)
GROUP.set_field('maxOpenSeverityFinding', max_open_severity_finding.resolve)
GROUP.set_field('maxSeverityFinding', max_severity_finding.resolve)
GROUP.set_field('maxSeverity', max_severity.resolve)
GROUP.set_field('organization', organization.resolve)
GROUP.set_field('serviceAttributes', service_attributes.resolve)
GROUP.set_field('stakeholders', stakeholders.resolve)
GROUP.set_field('totalFindings', total_findings.resolve)
GROUP.set_field('totalTreatment', total_treatment.resolve)
GROUP.set_field('userRole', user_role.resolve)
