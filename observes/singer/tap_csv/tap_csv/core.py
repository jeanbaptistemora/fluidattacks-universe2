import csv
from enum import (
    Enum,
)
from returns.pipeline import (
    pipe,
)
from singer_io.singer2 import (
    SingerEmitter,
    SingerRecord,
    SingerSchema,
)
from singer_io.singer2.json import (
    JsonObj,
    JsonValFactory,
    JsonValue,
)
from singer_io.singer2.json_schema import (
    JsonSchema,
    JsonSchemaFactory,
)
from tap_csv import (
    utils,
)
import tempfile
from typing import (
    Callable,
    Dict,
    IO,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Sequence,
)

LOG = utils.get_log(__name__)
emitter = SingerEmitter()


class ColumnType(Enum):
    FLOAT = "float"
    STRING = "string"
    NUMBER = "number"
    DATE_TIME = "datetime"
    INT = "integer"
    BOOL = "bool"


class MetadataRows(NamedTuple):
    field_names_row: int
    field_types_row: int
    pkeys_row: Optional[int] = None


class AdjustCsvOptions(NamedTuple):
    quote_nonnum: bool = False
    add_default_types: bool = False
    pkeys_present: bool = False
    only_records: bool = False
    file_schema: Dict[str, str] = {}


jlist = JsonValFactory.from_list


def translate_types(raw_field_type: Dict[str, ColumnType]) -> JsonSchema:
    """Translates type names into JSON SCHEMA types."""
    transform: Dict[ColumnType, JsonObj] = {
        ColumnType.STRING: {"type": JsonValue("string")},
        ColumnType.NUMBER: {"type": jlist(["number", "null"])},
        ColumnType.DATE_TIME: {"type": jlist(["string", "null"])},
        ColumnType.FLOAT: {"type": jlist(["number", "null"])},
        ColumnType.BOOL: {"type": JsonValue("boolean")},
        ColumnType.INT: {"type": jlist(["integer", "null"])},
    }
    field_type = {
        key: JsonValue(transform[val]).to_raw()
        for key, val in raw_field_type.items()
    }
    return JsonSchemaFactory.from_dict({"properties": field_type})


def translate_values(
    name_type_map: Dict[str, ColumnType],
    name_value_map: Dict[str, str],
    auto_type: bool = False,
) -> JsonObj:
    transform: Dict[ColumnType, Callable[[str], JsonValue]] = {
        ColumnType.STRING: pipe(JsonValue),
        ColumnType.NUMBER: pipe(lambda x: float(x) if x else None, JsonValue),
        ColumnType.DATE_TIME: pipe(JsonValue),
        ColumnType.FLOAT: pipe(lambda x: float(x) if x else None, JsonValue),
        ColumnType.BOOL: pipe(lambda x: bool(x) if x else None, JsonValue),
        ColumnType.INT: pipe(lambda x: int(x) if x else None, JsonValue),
    }

    def cast_function(name: str, value: str) -> JsonValue:
        if auto_type:
            return auto_cast(value)
        return transform[name_type_map[name]](value)

    new_name_value_map = map(
        lambda x: (x[0], cast_function(x[0], x[1])), name_value_map.items()
    )
    return dict(new_name_value_map)


def try_cast(cast: Callable[[str], JsonValue], data: str) -> JsonValue:
    try:
        return cast(data)
    except ValueError:
        return JsonValue(None)


def auto_cast(data: str) -> JsonValue:
    test_casts: List[Callable[[str], JsonValue]] = [
        pipe(lambda x: str(x) if int(x) > pow(10, 12) else int(x), JsonValue),
        pipe(
            lambda x: float(x)
            if (x.lower() != "nan" or x == "NaN") and float(x) != float("inf")
            else None,
            JsonValue,
        ),
        pipe(
            lambda x: x.lower() == "true"
            if x.lower() == "false" or x.lower() == "true"
            else None,
            JsonValue,
        ),
        pipe(JsonValue),
    ]
    cast: Callable[
        [Callable[[str], JsonValue]], JsonValue
    ] = lambda c: try_cast(c, data)
    return next(
        filter(lambda x: x.value is not None, map(cast, test_casts)),
        JsonValue(data),
    )


def add_default_types(
    field_names: Iterable[str], options: AdjustCsvOptions
) -> Dict[str, str]:
    field_types = map(
        lambda name: (
            name,
            options.file_schema.get(name.lower(), ColumnType.STRING.value),
        ),
        field_names,
    )
    result = dict(field_types)
    LOG.debug("added types: %s", result)
    return result


def adjust_csv(source: IO[str], options: AdjustCsvOptions) -> IO[str]:
    if not (options.quote_nonnum or options.add_default_types):
        return source
    source.seek(0)
    source_reader = csv.DictReader(source)
    field_names: Optional[Sequence[str]] = source_reader.fieldnames
    if not field_names:
        raise Exception()
    LOG.debug("field names: %s", field_names)
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(
            temp_dir + "/data.csv", "w+", encoding="UTF-8"
        ) as destination:
            dest_writer = csv.DictWriter(
                destination,
                field_names,
                quoting=csv.QUOTE_NONNUMERIC
                if options.quote_nonnum
                else csv.QUOTE_MINIMAL,
            )
            types_row: int = 3 if options.pkeys_present else 2
            dest_writer.writeheader()
            row_num = 1
            for row in source_reader:
                if row_num == types_row - 1 and options.add_default_types:
                    field_types = add_default_types(field_names, options)
                    LOG.debug("Write row: %s", field_types)
                    dest_writer.writerow(field_types)
                    row_num = row_num + 1
                dest_writer.writerow(row)
                row_num = row_num + 1
        with tempfile.NamedTemporaryFile("w+", delete=False) as output:
            with open(temp_dir + "/data.csv", "r", encoding="UTF-8") as file:
                output.write(file.read())
            return output


def to_singer(
    csv_file: IO[str],
    stream: str,
    options: AdjustCsvOptions,
) -> None:
    LOG.debug("csv file: %s", csv_file)
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
    reader = csv.reader(procesed_csv, delimiter=",", quotechar='"')
    meta_rows = MetadataRows(
        field_names_row=1,
        field_types_row=3 if options.pkeys_present else 2,
        pkeys_row=2 if options.pkeys_present else None,
    )
    LOG.debug("rows: %s", meta_rows)
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
                LOG.debug("name_type_map: %s", tuple(zip(field_names, record)))
                name_type_map = dict(
                    map(
                        lambda x: (x[0], ColumnType(x[1])),
                        zip(field_names, record),
                    )
                )
                if not options.only_records:
                    singer_schema: SingerSchema = SingerSchema(
                        stream=stream,
                        schema=translate_types(name_type_map),
                        key_properties=frozenset(pkeys),
                    )
                    emitter.emit(singer_schema)
        else:
            name_value_map = dict(zip(field_names, record))
            singer_record: SingerRecord = SingerRecord(
                stream=stream,
                record=translate_values(
                    name_type_map,
                    name_value_map,
                    auto_type=options.only_records,
                ),
            )
            emitter.emit(singer_record)
