# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.resolvers.event_evidence import (
    date,
)
from ariadne import (
    ObjectType,
)

EVENT_EVIDENCE_ITEM = ObjectType("EventEvidenceItem")
EVENT_EVIDENCE_ITEM.set_field("date", date.resolve)
