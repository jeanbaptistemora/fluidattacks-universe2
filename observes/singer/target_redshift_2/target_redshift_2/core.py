# Standard libraries
from typing import (
    IO,
    NamedTuple,
    Optional,
    Set,
)
# Third party libraries
# Local libraries=
from singer_io.singer import (
    SingerHandler,
    SingerRecord,
    SingerSchema,
    SingerState,
)
from singer_io.factory import singer_handler
from target_redshift_2.loader import Loader
from target_redshift_2.objects import InvalidState


class State(NamedTuple):
    current_schemas: Set[SingerSchema] = set()
    previous_record: Optional[SingerRecord] = None
    end_of_stream: bool = False


def schema_handler(
    singer: SingerSchema, state: State, loader: Loader
) -> State:
    loader.update_schema(singer)
    return State(
        current_schemas=state.current_schemas.union([singer]),
        previous_record=state.previous_record,
    )


def record_handler(
    singer: SingerRecord, state: State, loader: Loader
) -> State:
    if state.previous_record:
        loader.upload_record(state.previous_record, state.current_schemas)
    return State(
        current_schemas=state.current_schemas,
        previous_record=singer,
    )


def state_handler(
    singer: SingerState, state: State, loader: Loader
) -> State:
    if not state.previous_record:
        raise InvalidState('State msg should have a preceded record msg')
    loader.upload_and_save_state(
        state.previous_record,
        singer
    )
    return State(
        current_schemas=state.current_schemas,
        previous_record=None,
    )


def process_stdin(stdin: IO[str], loader: Loader) -> None:
    state: State = State()
    line: str = stdin.readline()

    def handle_schema(singer: SingerSchema, state: State) -> State:
        return schema_handler(singer, state, loader)

    def handle_record(singer: SingerRecord, state: State) -> State:
        return record_handler(singer, state, loader)

    handler: SingerHandler[State] = singer_handler(
        handle_schema, handle_record, None
    )
    while line:
        state = handler(line, state)
        line = stdin.readline()
    state = State(
        current_schemas=state.current_schemas,
        previous_record=state.previous_record,
        end_of_stream=True
    )
    handler(line, state)
