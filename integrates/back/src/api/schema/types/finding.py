# None


from api.resolvers.finding_new import (
    age_new,
    closed_vulnerabilities_new,
    consulting_new,
    current_state_new,
    cvss_version_new,
    evidence_new,
    group_name_new,
    hacker_new,
    historic_state_new,
    inputs_vulnerabilities_new,
    is_exploitable_new,
    last_vulnerability_new,
    lines_vulnerabilities_new,
    machine_jobs_new,
    observations_new,
    open_age_new,
    open_vulnerabilities_new,
    ports_vulnerabilities_new,
    records_new,
    release_date_new,
    remediated_new,
    report_date_new,
    severity_new,
    severity_score_new,
    sorts_new,
    status_new,
    tracking_new,
    treatment_summary_new,
    verified_new,
    vulnerabilities_new,
    vulnerabilities_to_reattack_new,
    where_new,
    zero_risk_new,
)
from ariadne import (
    ObjectType,
)

FINDING = ObjectType("Finding")

FINDING.set_field("age", age_new.resolve)
FINDING.set_field("closedVulnerabilities", closed_vulnerabilities_new.resolve)
FINDING.set_field("consulting", consulting_new.resolve)
FINDING.set_field("currentState", current_state_new.resolve)
FINDING.set_field("cvssVersion", cvss_version_new.resolve)
FINDING.set_field("evidence", evidence_new.resolve)
FINDING.set_field("groupName", group_name_new.resolve)
FINDING.set_field("hacker", hacker_new.resolve)
FINDING.set_field("historicState", historic_state_new.resolve)
FINDING.set_field("inputsVulnerabilities", inputs_vulnerabilities_new.resolve)
FINDING.set_field("isExploitable", is_exploitable_new.resolve)
FINDING.set_field("lastVulnerability", last_vulnerability_new.resolve)
FINDING.set_field("linesVulnerabilities", lines_vulnerabilities_new.resolve)
FINDING.set_field("machineJobs", machine_jobs_new.resolve)
FINDING.set_field("observations", observations_new.resolve)
FINDING.set_field("openAge", open_age_new.resolve)
FINDING.set_field("openVulnerabilities", open_vulnerabilities_new.resolve)
FINDING.set_field("portsVulnerabilities", ports_vulnerabilities_new.resolve)
FINDING.set_field("records", records_new.resolve)
FINDING.set_field("releaseDate", release_date_new.resolve)
FINDING.set_field("remediated", remediated_new.resolve)
FINDING.set_field("reportDate", report_date_new.resolve)
FINDING.set_field("severity", severity_new.resolve)
FINDING.set_field("severityScore", severity_score_new.resolve)
FINDING.set_field("sorts", sorts_new.resolve)
FINDING.set_field("state", status_new.resolve)
FINDING.set_field("tracking", tracking_new.resolve)
FINDING.set_field("treatmentSummary", treatment_summary_new.resolve)
FINDING.set_field("verified", verified_new.resolve)
FINDING.set_field("vulnerabilities", vulnerabilities_new.resolve)
FINDING.set_field(
    "vulnerabilitiesToReattack", vulnerabilities_to_reattack_new.resolve
)
FINDING.set_field("where", where_new.resolve)
FINDING.set_field("zeroRisk", zero_risk_new.resolve)
# --------------------------Deprecated fields------------------------------
FINDING.set_field("analyst", hacker_new.resolve)
FINDING.set_alias("attackVectorDesc", "attack_vector_description")
FINDING.set_field("inputsVulns", inputs_vulnerabilities_new.resolve)
FINDING.set_field("linesVulns", lines_vulnerabilities_new.resolve)
FINDING.set_field("newRemediated", remediated_new.resolve)
FINDING.set_field("portsVulns", ports_vulnerabilities_new.resolve)
FINDING.set_field("projectName", group_name_new.resolve)
FINDING.set_field("vulnsToReattack", vulnerabilities_to_reattack_new.resolve)
