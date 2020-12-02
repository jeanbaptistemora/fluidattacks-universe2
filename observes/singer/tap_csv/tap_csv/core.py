# Standard libraries
import csv
import tempfile
from typing import (
    Any,
    IO,
    NamedTuple,
    Optional,
    Sequence,
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


class AdjustCsvOptions(NamedTuple):
    quote_nonnum: bool = False
    add_default_types: bool = False
    pkeys_present: bool = False


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


def adjust_csv(source: IO[str], options: AdjustCsvOptions) -> IO[str]:
    if not(options.quote_nonnum or options.add_default_types):
        return source
    source.seek(0)
    source_reader = csv.DictReader(source)
    field_names: Optional[Sequence[str]] = source_reader.fieldnames
    if not field_names:
        raise Exception()
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
                if row_num == types_row and options.add_default_types:
                    field_types = dict(
                        zip(
                            field_names,
                            ['string' for _ in range(len(field_names))]
                        )
                    )
                    dest_writer.writerow(field_types)
                    row_num = row_num + 1
                dest_writer.writerow(row)
                row_num = row_num + 1
        output = tempfile.NamedTemporaryFile('w+')
        with open(temp_dir + '/data.csv', 'r') as destination:
            output.write(destination.read())
    output.flush()
    LOG.debug('output: %s', output.read()[0:2000])
    return output


def to_singer(
    csv_file: IO[str],
    stream: str,
    options: AdjustCsvOptions,
) -> None:
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
    reader = csv.reader(procesed_csv, delimiter=",", quotechar="\"")
    meta_rows = MetadataRows(
        field_names_row=1,
        field_types_row=3 if options.pkeys_present else 2,
        pkeys_row=2 if options.pkeys_present else None
    )
    row_num = 0
    pkeys = []
    field_names = []
    name_type_map = {}
    for record in reader:
        row_num += 1
        if row_num in frozenset(meta_rows):
            if row_num == meta_rows.field_names_row:
                field_names = record
            if row_num == meta_rows.pkeys_row:
                pkeys = record
            if row_num == meta_rows.field_types_row:
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
