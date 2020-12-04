# Standard libraries
import json
from typing import (
    Any,
    Dict,
    IO,
    NamedTuple,
)
# Third party libraries
# Local libraries
from tap_csv import core
from tap_csv.core import AdjustCsvOptions


class TapCsvInput(NamedTuple):
    stream: str
    csv_path: str
    options: AdjustCsvOptions


def deserialize(tap_input: str) -> TapCsvInput:
    """Generate `TapCsvInput` from json string"""
    raw_json: Dict[str, Any] = json.loads(tap_input)
    raw_json['options'] = AdjustCsvOptions(**raw_json['options'])
    return TapCsvInput(**raw_json)


def process_stdin(stdin: IO[str]) -> None:
    line: str = stdin.readline()
    while line:
        tap_input: TapCsvInput = deserialize(line)
        with open(tap_input.csv_path, 'r') as file:
            core.to_singer(file, tap_input.stream, tap_input.options)
        line = stdin.readline()
