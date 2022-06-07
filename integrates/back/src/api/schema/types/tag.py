# None


from api.resolvers.tag import (
    groups,
    last_closing_vuln,
    max_open_severity,
    max_severity,
    mean_remediate,
    mean_remediate_critical_severity,
    mean_remediate_high_severity,
    mean_remediate_low_severity,
    mean_remediate_medium_severity,
    name,
    organization,
)
from ariadne import (
    ObjectType,
)

TAG = ObjectType("Tag")
TAG.set_field("groups", groups.resolve)
TAG.set_field("name", name.resolve)
TAG.set_field("lastClosedVulnerability", last_closing_vuln.resolve)
TAG.set_field("maxOpenSeverity", max_open_severity.resolve)
TAG.set_field("maxSeverity", max_severity.resolve)
TAG.set_field("meanRemediate", mean_remediate.resolve)
TAG.set_field(
    "meanRemediateCriticalSeverity", mean_remediate_critical_severity.resolve
)
TAG.set_field(
    "meanRemediateHighSeverity", mean_remediate_high_severity.resolve
)
TAG.set_field("meanRemediateLowSeverity", mean_remediate_low_severity.resolve)
TAG.set_field(
    "meanRemediateMediumSeverity", mean_remediate_medium_severity.resolve
)
TAG.set_field("organization", organization.resolve)
