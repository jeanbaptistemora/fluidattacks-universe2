# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.toe_input import (
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

TOEINPUT = ObjectType("ToeInput")
TOEINPUT.set_field("attackedAt", attacked_at.resolve)
TOEINPUT.set_field("attackedBy", attacked_by.resolve)
TOEINPUT.set_field("bePresentUntil", be_present_until.resolve)
TOEINPUT.set_field("firstAttackAt", first_attack_at.resolve)
TOEINPUT.set_field("seenFirstTimeBy", seen_first_time_by.resolve)
TOEINPUT.set_field("root", root.resolve)
