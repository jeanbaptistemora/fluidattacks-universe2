from api.resolvers.group import (
    analytics,
    authors,
    closed_vulnerabilities,
    consulting,
    context,
    deletion_date,
    description,
    disambiguation,
    drafts,
    events,
    findings,
    forces_token,
    has_asm,
    language,
    last_closed_vulnerability,
    last_closed_vulnerability_finding,
    max_open_severity_finding,
    max_severity,
    max_severity_finding,
    organization,
    permissions,
    roots,
    service_attributes,
    stakeholders,
    toe_inputs,
    toe_lines,
    total_findings,
    total_treatment,
    user_role,
    vulnerabilities_assigned,
)
from ariadne import (
    ObjectType,
)

GROUP: ObjectType = ObjectType("Group")
GROUP.set_field("analytics", analytics.resolve)
GROUP.set_field("authors", authors.resolve)
GROUP.set_field("closedVulnerabilities", closed_vulnerabilities.resolve)
GROUP.set_field("consulting", consulting.resolve)
GROUP.set_field("deletionDate", deletion_date.resolve)
GROUP.set_field("description", description.resolve)
GROUP.set_field("disambiguation", disambiguation.resolve)
GROUP.set_field("drafts", drafts.resolve)
GROUP.set_field("events", events.resolve)
GROUP.set_field("findings", findings.resolve)
GROUP.set_field("forcesToken", forces_token.resolve)
GROUP.set_field("groupContext", context.resolve)
GROUP.set_field("hasAsm", has_asm.resolve)
GROUP.set_field("language", language.resolve)
GROUP.set_field(
    "lastClosedVulnerabilityFinding",
    last_closed_vulnerability_finding.resolve,
)
GROUP.set_field("lastClosedVulnerability", last_closed_vulnerability.resolve)
GROUP.set_field("maxOpenSeverityFinding", max_open_severity_finding.resolve)
GROUP.set_field("organization", organization.resolve)
GROUP.set_field("permissions", permissions.resolve)
GROUP.set_field("roots", roots.resolve)
GROUP.set_field("serviceAttributes", service_attributes.resolve)
GROUP.set_field("stakeholders", stakeholders.resolve)
GROUP.set_field("toeInputs", toe_inputs.resolve)
GROUP.set_field("toeLines", toe_lines.resolve)
GROUP.set_field("totalTreatment", total_treatment.resolve)
GROUP.set_field("userRole", user_role.resolve)

# --------------------------- Deprecated fields -------------------------------
GROUP.set_field("maxSeverity", max_severity.resolve)
GROUP.set_field("maxSeverityFinding", max_severity_finding.resolve)
GROUP.set_field("totalFindings", total_findings.resolve)
GROUP.set_field("vulnerabilitiesAssigned", vulnerabilities_assigned.resolve)
