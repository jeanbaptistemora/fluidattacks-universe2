# Standard libraries
import csv
import tempfile
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    IO,
    Iterable,
    NamedTuple,
    Optional,
    Sequence,
)
# Third party libraries
# Local libraries
from singer_io import factory
from singer_io.singer import (
    SingerRecord,
    SingerSchema,
)
from tap_csv import utils


LOG = utils.get_log(__name__)


class ColumnType(Enum):
    STRING = 'string'
    NUMBER = 'number'
    DATE_TIME = 'datetime'


class MetadataRows(NamedTuple):
    field_names_row: int
    field_types_row: int
    pkeys_row: Optional[int] = None


class AdjustCsvOptions(NamedTuple):
    quote_nonnum: bool = False
    add_default_types: bool = False
    pkeys_present: bool = False
    file_schema: Dict[str, str] = {}


def translate_types(
    raw_field_type: Dict[str, ColumnType]
) -> Dict[str, Dict[str, str]]:
    """Translates type names into JSON SCHEMA types."""
    type_string: Dict[str, str] = {"type": "string"}
    type_number: Dict[str, str] = {"type": "number"}
    type_datetime: Dict[str, str] = {
        "type": "string",
        "format": "date-time"
    }
    transform: Dict[ColumnType, Dict[str, str]] = {
        ColumnType.STRING: type_string,
        ColumnType.NUMBER: type_number,
        ColumnType.DATE_TIME: type_datetime
    }
    field_type = map(
        lambda x: (x[0], transform[x[1]]),
        raw_field_type.items()
    )
    return dict(field_type)


def translate_values(
    field_type: Dict[str, ColumnType],
    field_value: Dict[str, str]
) -> Dict[str, Any]:
    """Translates type names into JSON SCHEMA value."""
    transform: Dict[ColumnType, Callable[[str], Any]] = {
        ColumnType.STRING: lambda x: x,
        ColumnType.NUMBER: float,
        ColumnType.DATE_TIME: lambda x: x
    }
    new_field_value = map(
        lambda x: (x[0], transform[field_type[x[0]]](x[1])),
        field_value.items()
    )
    return dict(new_field_value)


def add_default_types(
    field_names: Iterable[str],
    options: AdjustCsvOptions
) -> Dict[str, str]:
    field_types = map(
        lambda name: (
            name,
            options.file_schema.get(
                name,
                ColumnType.STRING.value
            )
        ),
        field_names
    )
    return dict(field_types)


def adjust_csv(source: IO[str], options: AdjustCsvOptions) -> IO[str]:
    if not(options.quote_nonnum or options.add_default_types):
        return source
    source.seek(0)
    source_reader = csv.DictReader(source)
    field_names: Optional[Sequence[str]] = source_reader.fieldnames
    if not field_names:
        raise Exception()
    LOG.debug('field names: %s', field_names)
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(temp_dir + '/data.csv', 'w+') as destination:
            dest_writer = csv.DictWriter(
                destination,
                field_names,
                quoting=csv.QUOTE_NONNUMERIC
                if options.quote_nonnum else csv.QUOTE_MINIMAL
            )
            types_row: int = 3 if options.pkeys_present else 2
            dest_writer.writeheader()
            row_num = 1
            for row in source_reader:
                if row_num == types_row - 1 and options.add_default_types:
                    field_types = add_default_types(field_names, options)
                    dest_writer.writerow(field_types)
                    row_num = row_num + 1
                dest_writer.writerow(row)
                row_num = row_num + 1
        output = tempfile.NamedTemporaryFile('w+')
        with open(temp_dir + '/data.csv', 'r') as destination:
            output.write(destination.read())
    LOG.debug('output: %s', output.read()[0:2000])
    return output


def to_singer(
    csv_file: IO[str],
    stream: str,
    options: AdjustCsvOptions,
) -> None:
    LOG.debug('csv file: %s', csv_file)
    # ==== TAP ================================================================
    # line 1, field names
    # line 2, primary field(s)
    # line 3 (or 2 if pkeys are missing), field types:
    #           - string   "example"
    #           - number   "123.4"
    #           - datetime "2019-12-31T16:48:32Z" (MUST be RFC3339 compliant)
    # line >3, records
    # finally:
    #           - use "null" value with "string" type for empty cells
    procesed_csv: IO[str] = adjust_csv(csv_file, options)
    procesed_csv.seek(0)
    reader = csv.reader(procesed_csv, delimiter=",", quotechar="\"")
    meta_rows = MetadataRows(
        field_names_row=1,
        field_types_row=3 if options.pkeys_present else 2,
        pkeys_row=2 if options.pkeys_present else None
    )
    LOG.debug('rows: %s', meta_rows)
    row_num = 0
    pkeys = []
    field_names = []
    name_type_map: Dict[str, ColumnType] = {}
    name_value_map: Dict[str, str] = {}
    for record in reader:
        row_num += 1
        if row_num in frozenset(meta_rows):
            if row_num == meta_rows.field_names_row:
                field_names = record
            if row_num == meta_rows.pkeys_row:
                pkeys = record
            if row_num == meta_rows.field_types_row:
                name_type_map = dict(
                    map(
                        lambda x: (x[0], ColumnType(x[1])),
                        zip(field_names, record)
                    )
                )
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
