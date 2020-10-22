# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.finding import (
    analyst,
    closed_vulnerabilities,
    consulting,
    exploit,
    historic_state,
    inputs_vulns,
    lines_vulns,
    new_remediated,
    observations,
    open_vulnerabilities,
    pending_vulns,
    ports_vulns,
    records,
    vulnerabilities
)


FINDING = ObjectType('Finding')

FINDING.set_field('analyst', analyst.resolve)
FINDING.set_field('closedVulnerabilities', closed_vulnerabilities.resolve)
FINDING.set_field('consulting', consulting.resolve)
FINDING.set_field('exploit', exploit.resolve)
FINDING.set_field('historicState', historic_state.resolve)
FINDING.set_field('inputsVulns', inputs_vulns.resolve)
FINDING.set_field('linesVulns', lines_vulns.resolve)
FINDING.set_field('newRemediated', new_remediated.resolve)
FINDING.set_field('observations', observations.resolve)
FINDING.set_field('openVulnerabilities', open_vulnerabilities.resolve)
FINDING.set_field('pendingVulns', pending_vulns.resolve)
FINDING.set_field('portsVulns', ports_vulns.resolve)
FINDING.set_field('records', records.resolve)
FINDING.set_field('vulnerabilities', vulnerabilities.resolve)
