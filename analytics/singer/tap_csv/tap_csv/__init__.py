"""Singer tap for a CSV file.
"""

import csv
import sys
import json
import argparse

from typing import Any


# Type aliases that improve clarity
JSON = Any


def identity(obj: Any) -> Any:
    """Takes a single argument and returns it unchanged.

    Args:
        obj: any single argument.

    Returns:
        obj: exactly as it was provided.
    """
    return obj


def translate_types(field__type: JSON) -> JSON:
    """Translates type names into JSON SCHEMA types.
    """

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

    field__type = {f: dictionary[t] for f, t in field__type.items()}
    return field__type


def translate_values(field__type: JSON, field__value: JSON) -> JSON:
    """Translates type names into JSON SCHEMA value.
    """

    dictionary: JSON = {
        "string": identity,
        "number": float,
        "datetime": identity
    }

    new_field__value: JSON = {}
    for field_name, field_value in field__value.items():
        field_type: str = field__type[field_name]
        new_field__value[field_name] = dictionary[field_type](field_value)

    return new_field__value


def main():
    """Usual entry point.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-file',
        help='CSV file path')
    parser.add_argument(
        '-name',
        help='Table name')
    args = parser.parse_args()

    if not args.file or not args.name:
        parser.print_help()
        sys.exit(1)

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

    with open(args.file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="\"")

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
                    "stream": args.name,
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
                    "stream": args.name,
                    "record": field__value
                }
                print(json.dumps(singer_record))


if __name__ == "__main__":
    main()
