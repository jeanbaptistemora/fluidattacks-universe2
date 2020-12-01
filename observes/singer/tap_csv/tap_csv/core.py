import csv
import json
from typing import Any, IO


# Type aliases that improve clarity
JSON = Any


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


def to_singer(csv_file: IO[str], stream: str) -> None:
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
    reader = csv.reader(csv_file, delimiter=",", quotechar="\"")

    head_pos = 0
    field_main = []
    field_list = []
    field__type = {}
    field_jsontype_map = {}

    for record in reader:
        head_pos += 1
        if head_pos == 1:
            field_main = record
        elif head_pos == 2:
            field_list = record
        elif head_pos == 3:
            field__type = dict(zip(field_list, record))
            field_jsontype_map = translate_types(field__type)

            singer_schema: JSON = {
                "type": "SCHEMA",
                "stream": stream,
                "key_properties": field_main,
                "schema": {
                    "properties": field_jsontype_map
                }
            }
            print(json.dumps(singer_schema))
        else:
            field__value = {}

            index = 0
            for field_value in record:
                if not field_value == "null":
                    field__value[field_list[index]] = field_value
                index += 1

            field__value = translate_values(
                field__type, field__value)

            singer_record: JSON = {
                "type": "RECORD",
                "stream": stream,
                "record": field__value
            }
            print(json.dumps(singer_record))
