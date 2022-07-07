from api.resolvers.group import (
    analytics,
    authors,
    closed_vulnerabilities,
    consulting,
    context,
    credentials,
    deletion_date,
    drafts,
    events,
    findings,
    forces_token,
    has_asm,
    has_forces,
    has_machine,
    has_squad,
    language,
    last_closed_vulnerability,
    last_closed_vulnerability_finding,
    managed,
    max_open_severity,
    max_open_severity_finding,
    max_severity,
    max_severity_finding,
    mean_remediate,
    mean_remediate_critical_severity,
    mean_remediate_high_severity,
    mean_remediate_low_severity,
    mean_remediate_medium_severity,
    open_findings,
    open_vulnerabilities,
    organization,
    permissions,
    roots,
    service,
    service_attributes,
    stakeholders,
    subscription,
    tags,
    tier,
    toe_inputs,
    toe_lines,
    total_findings,
    total_treatment,
    user_deletion,
    user_role,
)
from ariadne import (
    ObjectType,
)

GROUP: ObjectType = ObjectType("Group")
GROUP.set_field("analytics", analytics.resolve)
GROUP.set_field("authors", authors.resolve)
GROUP.set_field("closedVulnerabilities", closed_vulnerabilities.resolve)
GROUP.set_field("consulting", consulting.resolve)
GROUP.set_field("credentials", credentials.resolve)
GROUP.set_field("deletionDate", deletion_date.resolve)
GROUP.set_field("drafts", drafts.resolve)
GROUP.set_field("events", events.resolve)
GROUP.set_field("findings", findings.resolve)
GROUP.set_field("forcesToken", forces_token.resolve)
GROUP.set_field("groupContext", context.resolve)
GROUP.set_field("hasAsm", has_asm.resolve)
GROUP.set_field("hasForces", has_forces.resolve)
GROUP.set_field("hasMachine", has_machine.resolve)
GROUP.set_field("hasSquad", has_squad.resolve)
GROUP.set_field("language", language.resolve)
GROUP.set_field(
    "lastClosedVulnerabilityFinding",
    last_closed_vulnerability_finding.resolve,
)
GROUP.set_field("lastClosedVulnerability", last_closed_vulnerability.resolve)
GROUP.set_field("managed", managed.resolve)
GROUP.set_field("maxOpenSeverity", max_open_severity.resolve)
GROUP.set_field("maxOpenSeverityFinding", max_open_severity_finding.resolve)
GROUP.set_field("meanRemediate", mean_remediate.resolve)
GROUP.set_field(
    "meanRemediateCriticalSeverity", mean_remediate_critical_severity.resolve
)
GROUP.set_field(
    "meanRemediateHighSeverity", mean_remediate_high_severity.resolve
)
GROUP.set_field(
    "meanRemediateLowSeverity", mean_remediate_low_severity.resolve
)
GROUP.set_field(
    "meanRemediateMediumSeverity", mean_remediate_medium_severity.resolve
)
GROUP.set_field("openFindings", open_findings.resolve)
GROUP.set_field("openVulnerabilities", open_vulnerabilities.resolve)
GROUP.set_field("organization", organization.resolve)
GROUP.set_field("permissions", permissions.resolve)
GROUP.set_field("roots", roots.resolve)
GROUP.set_field("service", service.resolve)
GROUP.set_field("serviceAttributes", service_attributes.resolve)
GROUP.set_field("subscription", subscription.resolve)
GROUP.set_field("stakeholders", stakeholders.resolve)
GROUP.set_field("tags", tags.resolve)
GROUP.set_field("tier", tier.resolve)
GROUP.set_field("toeInputs", toe_inputs.resolve)
GROUP.set_field("toeLines", toe_lines.resolve)
GROUP.set_field("totalTreatment", total_treatment.resolve)
GROUP.set_field("userDeletion", user_deletion.resolve)
GROUP.set_field("userRole", user_role.resolve)

# --------------------------- Deprecated fields -------------------------------
GROUP.set_field("maxSeverity", max_severity.resolve)
GROUP.set_field("maxSeverityFinding", max_severity_finding.resolve)
GROUP.set_field("totalFindings", total_findings.resolve)
