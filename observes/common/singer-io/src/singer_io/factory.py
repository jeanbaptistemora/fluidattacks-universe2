from collections.abc import (
    Callable,
)
import json
from singer_io import (
    _factory,
)
from singer_io.singer import (
    InvalidType,
    SingerHandler,
    SingerMessage,
    SingerRecord,
    SingerSchema,
    SingerState,
    State,
)
import sys
from typing import (
    Any,
    IO,
)


class UndefinedHandler(Exception):
    pass


def deserialize(singer_msg: str) -> SingerMessage:
    """Generate `SingerRecord` or `SingerSchema` from json string"""
    raw_json: dict[str, Any] = json.loads(singer_msg)
    data_type: str | None = raw_json.get("type", None)
    if data_type == "RECORD":
        return _factory.deserialize_record(singer_msg)
    if data_type == "SCHEMA":
        return _factory.deserialize_schema(singer_msg)
    if data_type == "STATE":
        return _factory.deserialize_state(singer_msg)
    raise InvalidType(
        f"Deserialize singer failed. Unknown or missing type '{data_type}'"
    )


def emit(singer_msg: SingerMessage, target: IO[str] = sys.stdout) -> None:
    msg_dict: dict[str, Any] = singer_msg._asdict()
    mapper = {
        SingerRecord: "RECORD",
        SingerSchema: "SCHEMA",
        SingerState: "STATE",
    }
    msg_dict["type"] = mapper[type(singer_msg)]
    msg = json.dumps(msg_dict, cls=_factory.CustomJsonEncoder)
    print(msg, file=target, flush=True)


def singer_handler(
    handle_schema: Callable[[SingerSchema, State], State] | None,
    handle_record: Callable[[SingerRecord, State], State] | None,
    handle_state: Callable[[SingerState, State], State] | None,
) -> SingerHandler[State]:
    def generic_handler(singer: SingerMessage, state: State) -> State:
        if handle_schema and isinstance(singer, SingerSchema):
            return handle_schema(singer, state)
        if handle_record and isinstance(singer, SingerRecord):
            return handle_record(singer, state)
        if handle_state and isinstance(singer, SingerState):
            return handle_state(singer, state)
        raise UndefinedHandler()

    def handle(line: str, state: State) -> State:
        singer_input: SingerMessage = deserialize(line)
        return generic_handler(singer_input, state)

    return handle
