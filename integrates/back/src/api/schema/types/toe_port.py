from api.resolvers.toe_port import (
    attacked_at,
    attacked_by,
    be_present_until,
    first_attack_at,
    root,
    seen_first_time_by,
)
from ariadne import (
    ObjectType,
)

TOEPORT = ObjectType("ToePort")
TOEPORT.set_field("attackedAt", attacked_at.resolve)
TOEPORT.set_field("attackedBy", attacked_by.resolve)
TOEPORT.set_field("bePresentUntil", be_present_until.resolve)
TOEPORT.set_field("firstAttackAt", first_attack_at.resolve)
TOEPORT.set_field("seenFirstTimeBy", seen_first_time_by.resolve)
TOEPORT.set_field("root", root.resolve)
