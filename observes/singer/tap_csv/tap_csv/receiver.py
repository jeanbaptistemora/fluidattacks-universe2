# Standard libraries
from typing import (
    Any,
    Dict,
    IO,
    NamedTuple,
)
# Third party libraries
# Local libraries
from singer_io import factory
from singer_io.singer import SingerRecord
from tap_csv import core, utils
from tap_csv.core import AdjustCsvOptions


LOG = utils.get_log(__name__)


class TapCsvInput(NamedTuple):
    stream: str
    csv_path: str
    options: AdjustCsvOptions


def deserialize(tap_input: str) -> TapCsvInput:
    """Generate `TapCsvInput` from json string"""
    singer_msg = factory.deserialize(tap_input)
    if not isinstance(singer_msg, SingerRecord):
        raise Exception('Expected `SingerRecord`')
    s_record: SingerRecord = singer_msg
    raw_json: Dict[str, Any] = s_record.record
    LOG.debug('Recieved %s', raw_json)
    raw_json['stream'] = s_record.stream
    raw_json['options'] = AdjustCsvOptions(**raw_json['options'])
    return TapCsvInput(**raw_json)


def process_stdin(stdin: IO[str]) -> None:
    line: str = stdin.readline()
    while line:
        tap_input: TapCsvInput = deserialize(line)
        LOG.debug('Tap input %s', tap_input)
        with open(tap_input.csv_path, 'r') as file:
            core.to_singer(file, tap_input.stream, tap_input.options)
        line = stdin.readline()
