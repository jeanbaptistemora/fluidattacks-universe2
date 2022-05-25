from fa_purity import (
    FrozenDict,
    JsonValue,
)
from fa_singer_io.json_schema.factory import (
    datetime_schema,
    from_json,
    from_prim_type,
)
from fa_singer_io.singer import (
    SingerSchema,
)
from tap_gitlab.singer.issues.core import (
    SingerStreams,
)


def issue_assignees() -> SingerSchema:
    properties = FrozenDict(
        {
            "issue_id": JsonValue(from_prim_type(str).encode()),
            "assignee": JsonValue(from_prim_type(str).encode()),
        }
    )
    schema = FrozenDict({"properties": JsonValue(properties)})
    return SingerSchema.new(
        SingerStreams.issue_assignees.value,
        from_json(schema).unwrap(),
        frozenset(["issue_id", "assignee"]),
        None,
    ).unwrap()


def issue_labels() -> SingerSchema:
    properties = FrozenDict(
        {
            "issue_id": JsonValue(from_prim_type(str).encode()),
            "label": JsonValue(from_prim_type(str).encode()),
        }
    )
    schema = FrozenDict({"properties": JsonValue(properties)})
    return SingerSchema.new(
        SingerStreams.issue_labels.value,
        from_json(schema).unwrap(),
        frozenset(["issue_id", "label"]),
        None,
    ).unwrap()


def issue() -> SingerSchema:
    properties = FrozenDict(
        {
            "id": JsonValue(from_prim_type(str).encode()),
            "iid": JsonValue(from_prim_type(int).encode()),
            "title": JsonValue(from_prim_type(str).encode()),
            "state": JsonValue(from_prim_type(str).encode()),
            "issue_type": JsonValue(from_prim_type(str).encode()),
            "confidential": JsonValue(from_prim_type(bool).encode()),
            "discussion_locked": JsonValue(from_prim_type(bool).encode()),
            "author_id": JsonValue(from_prim_type(str).encode()),
            "up_votes": JsonValue(from_prim_type(int).encode()),
            "down_votes": JsonValue(from_prim_type(int).encode()),
            "merge_requests_count": JsonValue(from_prim_type(int).encode()),
            "description": JsonValue(from_prim_type(str).encode()),
            "milestone_id": JsonValue(from_prim_type(str).encode()),
            "milestone_iid": JsonValue(from_prim_type(int).encode()),
            "due_date": JsonValue(datetime_schema().encode()),
            "epic_id": JsonValue(from_prim_type(str).encode()),
            "epic_iid": JsonValue(from_prim_type(int).encode()),
            "weight": JsonValue(from_prim_type(int).encode()),
            "created_at": JsonValue(datetime_schema().encode()),
            "updated_at": JsonValue(datetime_schema().encode()),
            "closed_at": JsonValue(datetime_schema().encode()),
            "closed_by": JsonValue(from_prim_type(str).encode()),
            "health_status": JsonValue(from_prim_type(str).encode()),
        }
    )
    schema = FrozenDict({"properties": JsonValue(properties)})
    return SingerSchema.new(
        SingerStreams.issue_labels.value,
        from_json(schema).unwrap(),
        frozenset(["id"]),
        None,
    ).unwrap()
