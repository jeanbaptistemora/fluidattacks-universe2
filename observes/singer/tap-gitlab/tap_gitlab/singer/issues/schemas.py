from fa_purity import (
    FrozenDict,
    JsonValue,
)
from fa_singer_io.json_schema.factory import (
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
