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
    ports_vulns
)


FINDING = ObjectType('Finding')

FINDING.set_field('closedVulnerabilities', closed_vulnerabilities.resolve)
FINDING.set_field('consulting', consulting.resolve)
FINDING.set_field('exploit', exploit.resolve)
FINDING.set_field('inputsVulns', inputs_vulns.resolve)
FINDING.set_field('linesVulns', lines_vulns.resolve)
FINDING.set_field('observations', observations.resolve)
FINDING.set_field('portsVulns', ports_vulns.resolve)
