# None


from api.resolvers.group import (
    analytics,
    bill,
    consulting,
    drafts,
    events,
    findings,
    findings_new,
    forces_token,
    last_closing_vuln_finding,
    max_open_severity_finding,
    max_severity,
    max_severity_finding,
    organization,
    roots,
    service_attributes,
    stakeholders,
    toe_inputs,
    total_findings,
    total_treatment,
    user_role,
)
from ariadne import (
    ObjectType,
)
from context import (
    FI_API_STATUS,
)

GROUP: ObjectType = ObjectType("Group")
GROUP.set_field("analytics", analytics.resolve)
GROUP.set_field("bill", bill.resolve)
GROUP.set_field("consulting", consulting.resolve)
GROUP.set_field("drafts", drafts.resolve)
GROUP.set_field("events", events.resolve)
GROUP.set_field("forcesToken", forces_token.resolve)
GROUP.set_field("lastClosingVulnFinding", last_closing_vuln_finding.resolve)
GROUP.set_field("maxOpenSeverityFinding", max_open_severity_finding.resolve)
GROUP.set_field("maxSeverityFinding", max_severity_finding.resolve)
GROUP.set_field("maxSeverity", max_severity.resolve)
GROUP.set_field("organization", organization.resolve)
GROUP.set_field("roots", roots.resolve)
GROUP.set_field("serviceAttributes", service_attributes.resolve)
GROUP.set_field("stakeholders", stakeholders.resolve)
GROUP.set_field("toeInputs", toe_inputs.resolve)
GROUP.set_field("totalFindings", total_findings.resolve)
GROUP.set_field("totalTreatment", total_treatment.resolve)
GROUP.set_field("userRole", user_role.resolve)

if FI_API_STATUS == "migration":
    GROUP.set_field("findings", findings_new.resolve)
else:
    GROUP.set_field("findings", findings.resolve)
