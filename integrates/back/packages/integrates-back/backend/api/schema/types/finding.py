# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.finding import (
    age,
    analyst,
    closed_vulnerabilities,
    consulting,
    exploit,
    historic_state,
    inputs_vulns,
    last_vulnerability,
    last_vuln_report,
    lines_vulns,
    new_remediated,
    observations,
    open_age,
    open_vulnerabilities,
    ports_vulns,
    records,
    release_date,
    report_date,
    sorts,
    state,
    tracking,
    verified,
    vulnerabilities
)


FINDING = ObjectType('Finding')

FINDING.set_field('age', age.resolve)
FINDING.set_field('analyst', analyst.resolve)
FINDING.set_field('closedVulnerabilities', closed_vulnerabilities.resolve)
FINDING.set_field('consulting', consulting.resolve)
FINDING.set_field('exploit', exploit.resolve)
FINDING.set_field('historicState', historic_state.resolve)
FINDING.set_field('inputsVulns', inputs_vulns.resolve)
FINDING.set_field('lastVulnerability', last_vulnerability.resolve)
FINDING.set_field('lastVulnReport', last_vuln_report.resolve)
FINDING.set_field('linesVulns', lines_vulns.resolve)
FINDING.set_field('newRemediated', new_remediated.resolve)
FINDING.set_field('observations', observations.resolve)
FINDING.set_field('openAge', open_age.resolve)
FINDING.set_field('openVulnerabilities', open_vulnerabilities.resolve)
FINDING.set_field('portsVulns', ports_vulns.resolve)
FINDING.set_field('records', records.resolve)
FINDING.set_field('releaseDate', release_date.resolve)
FINDING.set_field('reportDate', report_date.resolve)
FINDING.set_field('sorts', sorts.resolve)
FINDING.set_field('state', state.resolve)
FINDING.set_field('tracking', tracking.resolve)
FINDING.set_field('verified', verified.resolve)
FINDING.set_field('vulnerabilities', vulnerabilities.resolve)
