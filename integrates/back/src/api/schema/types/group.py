# None


from api.resolvers.group import (
    analytics,
    bill,
    consulting,
    drafts,
    events,
    findings,
    forces_token,
    last_closed_vulnerability_finding_new,
    max_open_severity_finding_new,
    max_severity_finding_new,
    max_severity_new,
    organization,
    permissions,
    roots,
    service_attributes,
    stakeholders,
    toe_inputs,
    toe_lines,
    total_findings_new,
    total_treatment,
    user_role,
)
from ariadne import (
    ObjectType,
)

GROUP: ObjectType = ObjectType("Group")
GROUP.set_field("analytics", analytics.resolve)
GROUP.set_field("bill", bill.resolve)
GROUP.set_field("consulting", consulting.resolve)
GROUP.set_field("drafts", drafts.resolve)
GROUP.set_field("events", events.resolve)
GROUP.set_field("findings", findings.resolve)
GROUP.set_field("forcesToken", forces_token.resolve)
GROUP.set_field("organization", organization.resolve)
GROUP.set_field(
    "lastClosedVulnerabilityFinding",
    last_closed_vulnerability_finding_new.resolve,
)
GROUP.set_field(
    "maxOpenSeverityFinding", max_open_severity_finding_new.resolve
)
GROUP.set_field("maxSeverity", max_severity_new.resolve)
GROUP.set_field("maxSeverityFinding", max_severity_finding_new.resolve)
GROUP.set_field("roots", roots.resolve)
GROUP.set_field("permissions", permissions.resolve)
GROUP.set_field("serviceAttributes", service_attributes.resolve)
GROUP.set_field("stakeholders", stakeholders.resolve)
GROUP.set_field("toeInputs", toe_inputs.resolve)
GROUP.set_field("toeLines", toe_lines.resolve)
GROUP.set_field("totalFindings", total_findings_new.resolve)
GROUP.set_field("totalTreatment", total_treatment.resolve)
GROUP.set_field("userRole", user_role.resolve)
GROUP.set_alias("lastClosedVulnerability", "last_closing_vuln")

# --------------------Deprecated fields------------------------------------
GROUP.set_field(
    "lastClosingVulnFinding", last_closed_vulnerability_finding_new.resolve
)
