# Standard
# None

# Third party
from ariadne import ObjectType

# Local
from backend.api.resolvers.new.finding import (
    closed_vulnerabilities,
    consulting,
    exploit,
    inputs_vulns,
    lines_vulns,
    observations,
    open_vulnerabilities,
    pending_vulns,
    ports_vulns,
    vulnerabilities
)


FINDING = ObjectType('Finding')

FINDING.set_field('closedVulnerabilities', closed_vulnerabilities.resolve)
FINDING.set_field('consulting', consulting.resolve)
FINDING.set_field('exploit', exploit.resolve)
FINDING.set_field('inputsVulns', inputs_vulns.resolve)
FINDING.set_field('linesVulns', lines_vulns.resolve)
FINDING.set_field('observations', observations.resolve)
FINDING.set_field('openVulnerabilities', open_vulnerabilities.resolve)
FINDING.set_field('pendingVulns', pending_vulns.resolve)
FINDING.set_field('portsVulns', ports_vulns.resolve)
FINDING.set_field('vulnerabilities', vulnerabilities.resolve)
