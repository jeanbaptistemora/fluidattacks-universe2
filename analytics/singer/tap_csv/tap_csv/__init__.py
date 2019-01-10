"""
Singer tap for a CSV file
"""

## python3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import csv
import json
import argparse

def translate_types(field_type_map):
    """ translates type names into JSON SCHEMA types """
    type_string = {"type": "string"}
    type_number = {"type": "number"}
    type_datetime = {"type": "string", "format": "date-time"}

    dictionary = {
        "string": type_string,
        "number": type_number,
        "datetime": type_datetime
    }

    new_field_type_map = {f: dictionary[t] for f, t in field_type_map.items()}
    return new_field_type_map

def translate_values(field_type_map, field_value_map):
    """ translates type names into JSON SCHEMA value """
    identity = lambda x: x

    dictionary = {
        "string": identity,
        "number": float,
        "datetime": identity
    }

    new_field_value_map = {}
    for field_name, field_value in field_value_map.items():
        field_type = field_type_map[field_name]
        new_field_value_map[field_name] = dictionary[field_type](field_value)

    return new_field_value_map

def main():
    """ usual entry point """

    # ==== User Interface =========================================================================
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
        exit(1)

    # ==== TAP ====================================================================================
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
        field_type_map = {}
        field_jsontype_map = {}

        for record in reader:
            head_pos += 1
            if head_pos == 1:
                field_main = record
            elif head_pos == 2:
                field_list = record
            elif head_pos == 3:
                field_type_map = dict(zip(field_list, record))
                field_jsontype_map = translate_types(field_type_map)

                singer_schema = {
                    "type": "SCHEMA",
                    "stream": args.name,
                    "key_properties": field_main,
                    "schema": {
                        "properties": field_jsontype_map
                    }
                }
                print(json.dumps(singer_schema))
            else:
                field_value_map = {}

                index = 0
                for field_value in record:
                    if not field_value == "null":
                        field_value_map[field_list[index]] = field_value
                    index += 1

                field_value_map = translate_values(field_type_map, field_value_map)

                singer_record = {
                    "type": "RECORD",
                    "stream": args.name,
                    "record": field_value_map
                }
                print(json.dumps(singer_record))

if __name__ == "__main__":
    main()
