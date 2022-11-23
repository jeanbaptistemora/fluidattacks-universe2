# None


from api.resolvers.finding import (
    age,
    closed_vulnerabilities,
    consulting,
    current_state,
    cvss_version,
    evidence,
    group_name,
    hacker,
    historic_state,
    is_exploitable,
    last_vulnerability,
    machine_jobs,
    observations,
    open_age,
    open_vulnerabilities,
    records,
    release_date,
    remediated,
    report_date,
    severity,
    severity_score,
    sorts,
    status,
    tracking,
    treatment_summary,
    verification_summary,
    verified,
    vulnerabilities_connection,
    vulnerabilities_to_reattack_connection,
    where,
    zero_risk_connection,
)
from ariadne import (
    ObjectType,
)

FINDING = ObjectType("Finding")

FINDING.set_field("age", age.resolve)
FINDING.set_field("closedVulnerabilities", closed_vulnerabilities.resolve)
FINDING.set_field("consulting", consulting.resolve)
FINDING.set_field("currentState", current_state.resolve)
FINDING.set_field("cvssVersion", cvss_version.resolve)
FINDING.set_field("evidence", evidence.resolve)
FINDING.set_field("groupName", group_name.resolve)
FINDING.set_field("hacker", hacker.resolve)
FINDING.set_field("historicState", historic_state.resolve)
FINDING.set_field("isExploitable", is_exploitable.resolve)
FINDING.set_field("lastVulnerability", last_vulnerability.resolve)
FINDING.set_field("machineJobs", machine_jobs.resolve)
FINDING.set_field("observations", observations.resolve)
FINDING.set_field("openAge", open_age.resolve)
FINDING.set_field("openVulnerabilities", open_vulnerabilities.resolve)
FINDING.set_field("records", records.resolve)
FINDING.set_field("releaseDate", release_date.resolve)
FINDING.set_field("remediated", remediated.resolve)
FINDING.set_field("reportDate", report_date.resolve)
FINDING.set_field("severity", severity.resolve)
FINDING.set_field("severityScore", severity_score.resolve)
FINDING.set_field("sorts", sorts.resolve)
FINDING.set_field("state", status.resolve)
FINDING.set_field("tracking", tracking.resolve)
FINDING.set_field("treatmentSummary", treatment_summary.resolve)
FINDING.set_field("verificationSummary", verification_summary.resolve)
FINDING.set_field("verified", verified.resolve)
FINDING.set_field(
    "vulnerabilitiesConnection", vulnerabilities_connection.resolve
)
FINDING.set_field(
    "vulnerabilitiesToReattackConnection",
    vulnerabilities_to_reattack_connection.resolve,
)
FINDING.set_field("where", where.resolve)
FINDING.set_field("zeroRiskConnection", zero_risk_connection.resolve)
