# None


from api.resolvers.finding import (
    age,
    analyst,
    closed_vulnerabilities,
    consulting,
    historic_state,
    inputs_vulns,
    last_vulnerability,
    lines_vulns,
    machine_jobs,
    new_remediated,
    observations,
    open_age,
    open_vulnerabilities,
    ports_vulns,
    records,
    release_date,
    remediated,
    report_date,
    sorts,
    state,
    tracking,
    verified,
    vulnerabilities,
    vulns_to_reattack,
    zero_risk,
)
from api.resolvers.finding_new import (
    age_new,
    analyst_new,
    closed_vulnerabilities_new,
    consulting_new,
    current_state_new,
    evidence_new,
    group_name_new,
    historic_state_new,
    inputs_vulns_new,
    is_exploitable_new,
    last_vulnerability_new,
    lines_vulns_new,
    machine_jobs_new,
    observations_new,
    open_age_new,
    open_vulnerabilities_new,
    ports_vulns_new,
    records_new,
    release_date_new,
    remediated_new,
    report_date_new,
    severity_new,
    severity_score_new,
    sorts_new,
    status_new,
    tracking_new,
    verified_new,
    vulnerabilities_new,
    vulns_to_reattack_new,
    zero_risk_new,
)
from ariadne import (
    ObjectType,
)
from context import (
    FI_API_STATUS,
)

FINDING = ObjectType("Finding")


if FI_API_STATUS == "migration":
    FINDING.set_field("age", age_new.resolve)
    FINDING.set_field("analyst", analyst_new.resolve)
    FINDING.set_field(
        "closedVulnerabilities", closed_vulnerabilities_new.resolve
    )
    FINDING.set_field("consulting", consulting_new.resolve)
    FINDING.set_field("currentState", current_state_new.resolve)
    FINDING.set_field("evidence", evidence_new.resolve)
    FINDING.set_field("historicState", historic_state_new.resolve)
    FINDING.set_field("inputsVulns", inputs_vulns_new.resolve)
    FINDING.set_field("isExploitable", is_exploitable_new.resolve)
    FINDING.set_field("lastVulnerability", last_vulnerability_new.resolve)
    FINDING.set_field("linesVulns", lines_vulns_new.resolve)
    FINDING.set_field("machineJobs", machine_jobs_new.resolve)
    FINDING.set_field("newRemediated", remediated_new.resolve)
    FINDING.set_field("observations", observations_new.resolve)
    FINDING.set_field("openAge", open_age_new.resolve)
    FINDING.set_field("openVulnerabilities", open_vulnerabilities_new.resolve)
    FINDING.set_field("portsVulns", ports_vulns_new.resolve)
    FINDING.set_field("projectName", group_name_new.resolve)
    FINDING.set_field("records", records_new.resolve)
    FINDING.set_field("releaseDate", release_date_new.resolve)
    FINDING.set_field("remediated", remediated_new.resolve)
    FINDING.set_field("reportDate", report_date_new.resolve)
    FINDING.set_field("severity", severity_new.resolve)
    FINDING.set_field("severityScore", severity_score_new.resolve)
    FINDING.set_field("sorts", sorts_new.resolve)
    FINDING.set_field("state", status_new.resolve)
    FINDING.set_field("tracking", tracking_new.resolve)
    FINDING.set_field("verified", verified_new.resolve)
    FINDING.set_field("vulnerabilities", vulnerabilities_new.resolve)
    FINDING.set_field("zeroRisk", zero_risk_new.resolve)
    FINDING.set_field("vulnsToReattack", vulns_to_reattack_new.resolve)
    # Standardization field
    FINDING.set_field("groupName", group_name_new.resolve)
else:
    FINDING.set_field("age", age.resolve)
    FINDING.set_field("analyst", analyst.resolve)
    FINDING.set_field("closedVulnerabilities", closed_vulnerabilities.resolve)
    FINDING.set_field("consulting", consulting.resolve)
    FINDING.set_field("historicState", historic_state.resolve)
    FINDING.set_field("inputsVulns", inputs_vulns.resolve)
    FINDING.set_field("lastVulnerability", last_vulnerability.resolve)
    FINDING.set_field("linesVulns", lines_vulns.resolve)
    FINDING.set_field("machineJobs", machine_jobs.resolve)
    FINDING.set_field("newRemediated", new_remediated.resolve)
    FINDING.set_field("observations", observations.resolve)
    FINDING.set_field("openAge", open_age.resolve)
    FINDING.set_field("openVulnerabilities", open_vulnerabilities.resolve)
    FINDING.set_field("portsVulns", ports_vulns.resolve)
    FINDING.set_field("records", records.resolve)
    FINDING.set_field("releaseDate", release_date.resolve)
    FINDING.set_field("remediated", remediated.resolve)
    FINDING.set_field("reportDate", report_date.resolve)
    FINDING.set_field("sorts", sorts.resolve)
    FINDING.set_field("state", state.resolve)
    FINDING.set_field("tracking", tracking.resolve)
    FINDING.set_field("verified", verified.resolve)
    FINDING.set_field("vulnerabilities", vulnerabilities.resolve)
    FINDING.set_field("zeroRisk", zero_risk.resolve)
    FINDING.set_field("vulnsToReattack", vulns_to_reattack.resolve)
