# Standard libraries
import json
import sys
from typing import (
    Any,
    Dict,
    IO,
    Mapping,
    Optional,
    Type,
)
# Third party libraries
# Local libraries
from singer_io.singer import (
    InvalidType,
    ProcessSinger,
    SingerHandler,
    SingerMessage,
    SingerRecord,
    SingerSchema,
    SingerState,
    State
)
from singer_io import _factory


def deserialize(singer_msg: str) -> SingerMessage:
    """Generate `SingerRecord` or `SingerSchema` from json string"""
    raw_json: Dict[str, Any] = json.loads(singer_msg)
    data_type: Optional[str] = raw_json.get('type', None)
    if data_type == 'RECORD':
        return _factory.deserialize_record(singer_msg)
    if data_type == 'SCHEMA':
        return _factory.deserialize_schema(singer_msg)
    if data_type == 'STATE':
        return _factory.deserialize_state(singer_msg)
    raise InvalidType(
        f'Deserialize singer failed. Unknown or missing type \'{data_type}\''
    )


def emit(singer_msg: SingerMessage, target: IO[str] = sys.stdout) -> None:
    msg_dict: Dict[str, Any] = singer_msg._asdict()
    mapper = {
        SingerRecord: 'RECORD',
        SingerSchema: 'SCHEMA',
        SingerState: 'STATE',
    }
    msg_dict['type'] = mapper[type(singer_msg)]
    msg = json.dumps(msg_dict, cls=_factory.CustomJsonEncoder)
    print(msg, file=target, flush=True)


def singer_handler(
    handlers: Mapping[Type[SingerMessage], ProcessSinger[State]]
) -> SingerHandler[State]:
    def handle(line: str, state: State) -> State:
        singer_input: SingerMessage = deserialize(line)
        input_handler: ProcessSinger[State] = handlers[type(singer_input)]
        return input_handler(singer_input, state)
    return handle
