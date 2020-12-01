# Standard libraries
import csv
import tempfile
from typing import (
    Any,
    IO, NamedTuple, Optional,
)
# Third party libraries
# Local libraries
from tap_csv import utils
from singer_io import factory
from singer_io.singer import (
    SingerRecord,
    SingerSchema,
)


LOG = utils.get_log(__name__)
JSON = Any


class MetadataRows(NamedTuple):
    field_names_row: int
    field_types_row: int
    pkeys_row: Optional[int] = None


def translate_types(raw_field_type: JSON) -> JSON:
    """Translates type names into JSON SCHEMA types."""
    type_string: JSON = {
        "type": "string"
    }
    type_number: JSON = {
        "type": "number"
    }
    type_datetime: JSON = {
        "type": "string",
        "format": "date-time"
    }
    dictionary: JSON = {
        "string": type_string,
        "number": type_number,
        "datetime": type_datetime
    }
    field_type = {f: dictionary[t] for f, t in raw_field_type.items()}
    return field_type


def translate_values(field__type: JSON, field__value: JSON) -> JSON:
    """Translates type names into JSON SCHEMA value.
    """

    dictionary: JSON = {
        "string": lambda x: x,
        "number": float,
        "datetime": lambda x: x
    }

    new_field__value: JSON = {}
    for field_name, field_value in field__value.items():
        field_type: str = field__type[field_name]
        new_field__value[field_name] = dictionary[field_type](field_value)

    return new_field__value


def adjust_csv(file: IO[str]) -> IO[str]:
    # temporal interface
    return file


def to_singer(
    csv_file: IO[str],
    stream: str,
    special_rows: MetadataRows,
    quote_nonnum: bool,
) -> None:
    # ==== TAP ================================================================
    # line 1, primary field(s)
    # line 2, field names
    # line 3, field types:
    #           - string   "example"
    #           - number   "123.4"
    #           - datetime "2019-12-31T16:48:32Z" (MUST be RFC3339 compliant)
    # line >3, records
    # finally:
    #           - use "null" value with "string" type for empty cells
    procesed_csv: IO[str] = adjust_csv(csv_file) if quote_nonnum else csv_file
    reader = csv.reader(procesed_csv, delimiter=",", quotechar="\"")

    head_pos = 0
    pkeys = []
    field_names = []
    name_type_map = {}
    for record in reader:
        head_pos += 1
        if head_pos in frozenset(special_rows):
            if head_pos == special_rows.pkeys_row:
                pkeys = record
            if head_pos == special_rows.field_names_row:
                field_names = record
            if head_pos == special_rows.field_types_row:
                name_type_map = dict(zip(field_names, record))
                singer_schema: SingerSchema = SingerSchema(
                    stream=stream,
                    schema={
                        "properties": translate_types(name_type_map)
                    },
                    key_properties=frozenset(pkeys)
                )
                factory.emit(singer_schema)
        else:
            name_value_map = dict(zip(field_names, record))
            singer_record: SingerRecord = SingerRecord(
                stream=stream,
                record=translate_values(
                    name_type_map, name_value_map
                )
            )
            factory.emit(singer_record)
