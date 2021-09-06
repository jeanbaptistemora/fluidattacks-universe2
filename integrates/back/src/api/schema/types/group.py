# None


from api.resolvers.group import (
    analytics,
    bill,
    consulting,
    drafts,
    drafts_new,
    events,
    findings,
    findings_new,
    forces_token,
    last_closed_vulnerability_finding,
    last_closed_vulnerability_finding_new,
    max_open_severity_finding,
    max_open_severity_finding_new,
    max_severity,
    max_severity_finding,
    max_severity_finding_new,
    max_severity_new,
    organization,
    permissions,
    roots,
    service_attributes,
    stakeholders,
    toe_inputs,
    total_findings,
    total_findings_new,
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
GROUP.set_field("events", events.resolve)
GROUP.set_field("forcesToken", forces_token.resolve)
GROUP.set_field("organization", organization.resolve)
GROUP.set_field("roots", roots.resolve)
GROUP.set_field("permissions", permissions.resolve)
GROUP.set_field("serviceAttributes", service_attributes.resolve)
GROUP.set_field("stakeholders", stakeholders.resolve)
GROUP.set_field("toeInputs", toe_inputs.resolve)
GROUP.set_field("totalTreatment", total_treatment.resolve)
GROUP.set_field("userRole", user_role.resolve)
GROUP.set_alias("lastClosedVulnerability", "last_closing_vuln")

if FI_API_STATUS == "migration":
    GROUP.set_field("drafts", drafts_new.resolve)
    GROUP.set_field("findings", findings_new.resolve)
    GROUP.set_field(
        "lastClosedVulnerabilityFinding",
        last_closed_vulnerability_finding_new.resolve,
    )
    GROUP.set_field(
        "maxOpenSeverityFinding", max_open_severity_finding_new.resolve
    )
    GROUP.set_field("maxSeverity", max_severity_new.resolve)
    GROUP.set_field("maxSeverityFinding", max_severity_finding_new.resolve)
    GROUP.set_field("totalFindings", total_findings_new.resolve)
    # --------------------Deprecated fields------------------------------------
    GROUP.set_field(
        "lastClosingVulnFinding", last_closed_vulnerability_finding_new.resolve
    )
    # -------------------------------------------------------------------------
else:
    GROUP.set_field("drafts", drafts.resolve)
    GROUP.set_field("findings", findings.resolve)
    GROUP.set_field(
        "lastClosedVulnerabilityFinding",
        last_closed_vulnerability_finding.resolve,
    )
    GROUP.set_field(
        "maxOpenSeverityFinding", max_open_severity_finding.resolve
    )
    GROUP.set_field("maxSeverity", max_severity.resolve)
    GROUP.set_field("maxSeverityFinding", max_severity_finding.resolve)
    GROUP.set_field("totalFindings", total_findings.resolve)
    # ----------------------Deprecated fields----------------------------------
    GROUP.set_field(
        "lastClosingVulnFinding", last_closed_vulnerability_finding.resolve
    )
