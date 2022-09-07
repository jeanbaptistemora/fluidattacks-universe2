# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.toe_lines import (
    attacked_at,
    attacked_by,
    attacked_lines,
    be_present_until,
    comments,
    first_attack_at,
    root,
)
from ariadne import (
    ObjectType,
)

TOELINES = ObjectType("ToeLines")
TOELINES.set_field("attackedAt", attacked_at.resolve)
TOELINES.set_field("attackedBy", attacked_by.resolve)
TOELINES.set_field("attackedLines", attacked_lines.resolve)
TOELINES.set_field("bePresentUntil", be_present_until.resolve)
TOELINES.set_field("comments", comments.resolve)
TOELINES.set_field("firstAttackAt", first_attack_at.resolve)
TOELINES.set_field("root", root.resolve)
