from api.resolvers.event import (
    accessibility,
    affected_components,
    affected_reattacks,
    client,
    closing_date,
    consulting,
    detail,
    event_date,
    event_id,
    event_status,
    event_type,
    evidence,
    evidence_date,
    evidence_file,
    evidence_file_date,
    group_name,
    hacker,
    other_solving_reason,
    root,
    solving_reason,
)
from ariadne import (
    ObjectType,
)

EVENT = ObjectType("Event")
EVENT.set_field("accessibility", accessibility.resolve)
EVENT.set_field("affectedComponents", affected_components.resolve)
EVENT.set_field("client", client.resolve)
EVENT.set_field("closingDate", closing_date.resolve)
EVENT.set_field("detail", detail.resolve)
EVENT.set_field("eventDate", event_date.resolve)
EVENT.set_field("eventStatus", event_status.resolve)
EVENT.set_field("eventType", event_type.resolve)
EVENT.set_field("evidence", evidence.resolve)
EVENT.set_field("evidenceDate", evidence_date.resolve)
EVENT.set_field("evidenceFile", evidence_file.resolve)
EVENT.set_field("evidenceFileDate", evidence_file_date.resolve)
EVENT.set_field("groupName", group_name.resolve)
EVENT.set_field("hacker", hacker.resolve)
EVENT.set_field("id", event_id.resolve)
EVENT.set_field("affectedReattacks", affected_reattacks.resolve)
EVENT.set_field("consulting", consulting.resolve)
EVENT.set_field("otherSolvingReason", other_solving_reason.resolve)
EVENT.set_field("root", root.resolve)
EVENT.set_field("solvingReason", solving_reason.resolve)
