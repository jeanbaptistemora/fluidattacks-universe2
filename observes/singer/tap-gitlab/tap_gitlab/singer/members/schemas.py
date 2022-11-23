from .core import (
    SingerStreams,
)
from fa_purity import (
    FrozenDict,
    JsonValue,
    PureIter,
)
from fa_purity.pure_iter.factory import (
    from_list,
)
from fa_singer_io.json_schema.factory import (
    datetime_schema,
    from_json,
    from_prim_type,
    opt_prim_type,
)
from fa_singer_io.singer import (
    SingerSchema,
)


def members() -> SingerSchema:
    properties: FrozenDict[str, JsonValue] = FrozenDict(
        {
            "project_id": JsonValue(from_prim_type(str).encode()),
            "user_id": JsonValue(from_prim_type(int).encode()),
            "username": JsonValue(from_prim_type(str).encode()),
            "email": JsonValue(opt_prim_type(str).encode()),
            "name": JsonValue(from_prim_type(str).encode()),
            "state": JsonValue(from_prim_type(str).encode()),
            "created_at": JsonValue(datetime_schema().encode()),
            "membership_state": JsonValue(from_prim_type(str).encode()),
        }
    )
    schema = FrozenDict({"properties": JsonValue(properties)})
    return SingerSchema.new(
        SingerStreams.members.value,
        from_json(schema).unwrap(),
        frozenset(["project_id", "user_id"]),
        None,
    ).unwrap()


def all_schemas() -> PureIter[SingerSchema]:
    return from_list([members()])
