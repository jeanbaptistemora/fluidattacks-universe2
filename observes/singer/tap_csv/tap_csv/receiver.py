from singer_io.singer2 import (
    SingerRecord,
)
from singer_io.singer2.deserializer import (
    SingerDeserializer,
)
import sys
from tap_csv import (
    core,
    utils,
)
from tap_csv.core import (
    AdjustCsvOptions,
)
from typing import (
    IO,
    NamedTuple,
    Optional,
)

LOG = utils.get_log(__name__)


class TapCsvInput(NamedTuple):
    stream: str
    csv_path: str
    options: AdjustCsvOptions


def _extract_options(record: SingerRecord) -> AdjustCsvOptions:
    opt = record.record["options"].to_json()
    quote_nonnum = opt.get("quote_nonnum")
    add_default_types = opt.get("add_default_types")
    pkeys_present = opt.get("pkeys_present")
    only_records = opt.get("only_records")
    file_schema = opt.get("file_schema")
    return AdjustCsvOptions(
        quote_nonnum.to_primitive(bool) if quote_nonnum else False,
        add_default_types.to_primitive(bool) if add_default_types else False,
        pkeys_present.to_primitive(bool) if pkeys_present else False,
        only_records.to_primitive(bool) if only_records else False,
        file_schema.to_dict_of(str) if file_schema else {},
    )


def deserialize(tap_input: str) -> Optional[TapCsvInput]:
    """Generate `TapCsvInput` from json string"""
    singer_msg = SingerDeserializer.deserialize(tap_input)
    if not isinstance(singer_msg, SingerRecord):
        raise Exception("Expected `SingerRecord`")
    s_record: SingerRecord = singer_msg
    LOG.debug("Recieved %s", s_record.record)
    if "csv_path" not in s_record.record:
        return None
    return TapCsvInput(
        s_record.stream,
        s_record.record["csv_path"].to_primitive(str),
        _extract_options(s_record),
    )


def process_stdin(stdin: IO[str]) -> None:
    line: str = stdin.readline()
    while line:
        tap_input = deserialize(line)
        if not tap_input:
            print(line, file=sys.stdout, flush=True)
            line = stdin.readline()
            continue
        LOG.debug("Tap input %s", tap_input)
        with open(tap_input.csv_path, "r", encoding="UTF-8") as file:
            core.to_singer(file, tap_input.stream, tap_input.options)
        line = stdin.readline()
