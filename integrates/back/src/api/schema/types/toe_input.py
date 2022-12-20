from api.resolvers.toe_input import (
    attacked_at,
    attacked_by,
    be_present,
    be_present_until,
    first_attack_at,
    has_vulnerabilities,
    root,
    seen_at,
    seen_first_time_by,
)
from ariadne import (
    ObjectType,
)

TOEINPUT = ObjectType("ToeInput")
TOEINPUT.set_field("attackedAt", attacked_at.resolve)
TOEINPUT.set_field("attackedBy", attacked_by.resolve)
TOEINPUT.set_field("bePresent", be_present.resolve)
TOEINPUT.set_field("bePresentUntil", be_present_until.resolve)
TOEINPUT.set_field("firstAttackAt", first_attack_at.resolve)
TOEINPUT.set_field("hasVulnerabilities", has_vulnerabilities.resolve)
TOEINPUT.set_field("root", root.resolve)
TOEINPUT.set_field("seenAt", seen_at.resolve)
TOEINPUT.set_field("seenFirstTimeBy", seen_first_time_by.resolve)
