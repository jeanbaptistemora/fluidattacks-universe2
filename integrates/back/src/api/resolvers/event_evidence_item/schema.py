from api.resolvers.event_evidence_item import (
    date,
)
from ariadne import (
    ObjectType,
)

EVENT_EVIDENCE_ITEM = ObjectType("EventEvidenceItem")
EVENT_EVIDENCE_ITEM.set_field("date", date.resolve)
