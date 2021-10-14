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
    inputs_vulnerabilities,
    is_exploitable,
    last_vulnerability,
    lines_vulnerabilities,
    machine_jobs,
    observations,
    open_age,
    open_vulnerabilities,
    ports_vulnerabilities,
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
    verified,
    vulnerabilities,
    vulnerabilities_to_reattack,
    where,
    zero_risk,
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
FINDING.set_field("inputsVulnerabilities", inputs_vulnerabilities.resolve)
FINDING.set_field("isExploitable", is_exploitable.resolve)
FINDING.set_field("lastVulnerability", last_vulnerability.resolve)
FINDING.set_field("linesVulnerabilities", lines_vulnerabilities.resolve)
FINDING.set_field("machineJobs", machine_jobs.resolve)
FINDING.set_field("observations", observations.resolve)
FINDING.set_field("openAge", open_age.resolve)
FINDING.set_field("openVulnerabilities", open_vulnerabilities.resolve)
FINDING.set_field("portsVulnerabilities", ports_vulnerabilities.resolve)
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
FINDING.set_field("verified", verified.resolve)
FINDING.set_field("vulnerabilities", vulnerabilities.resolve)
FINDING.set_field(
    "vulnerabilitiesToReattack", vulnerabilities_to_reattack.resolve
)
FINDING.set_field("where", where.resolve)
FINDING.set_field("zeroRisk", zero_risk.resolve)
# --------------------------Deprecated fields------------------------------
FINDING.set_field("analyst", hacker.resolve)
FINDING.set_alias("attackVectorDesc", "attack_vector_description")
FINDING.set_field("inputsVulns", inputs_vulnerabilities.resolve)
FINDING.set_field("linesVulns", lines_vulnerabilities.resolve)
FINDING.set_field("newRemediated", remediated.resolve)
FINDING.set_field("portsVulns", ports_vulnerabilities.resolve)
FINDING.set_field("projectName", group_name.resolve)
FINDING.set_field("vulnsToReattack", vulnerabilities_to_reattack.resolve)
