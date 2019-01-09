"""
Singer tap for AWS Dynamo DB
"""

## python3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

# pylint: disable=import-error

import re
import ast
import json
import argparse

from uuid     import uuid4    as gen_id
from datetime import datetime

import boto3 as AWS_SDK

from . import logs


_TYPE = {
    "string": {"type": "string"},
    "number": {"type": "number"},
    "date-time": {"type": "string", "format": "date-time"},

    "set": {"type": "string"},
    "list": {"type": "string"},
    "list<dict>": {"type": "string"},
}

def create_access_point(auth_keys):
    """ creates an access point to DynamoDB """

    session = AWS_SDK.session.Session(
        aws_access_key_id=auth_keys.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=auth_keys.get("AWS_SECRET_ACCESS_KEY"),
        region_name=auth_keys.get("AWS_DEFAULT_REGION")
    )

    dynamodb_client = session.client('dynamodb')
    dynamodb_resource = session.resource('dynamodb')

    return (dynamodb_client, dynamodb_resource)

def get_all_tables(dynamodb_client):
    """ returns a list with the names of all tables in the account """

    response = dynamodb_client.list_tables()

    table_list = response["TableNames"]
    while 'LastEvaluatedKey' in response:
        response = dynamodb_client.list_tables(
            ExclusiveStartTableName=response["LastEvaluatedTableName"],
            Limit=10
        )
        table_list.append(response["TableNames"])

    return table_list

def write_queries(dynamodb_resource, table_name):
    """ write queries to a file so it can be fast accessed later """
    def write(batch):
        """ since AWS works in batch, then we have to write this function """
        for json_obj in batch:
            stdout_json_obj = {}
            for key, val in json_obj.items():
                stdout_json_obj[key] = str(val)
            logs.log_json_obj(table_name, stdout_json_obj)

    table = dynamodb_resource.Table(table_name)

    response = table.scan()
    batch = response["Items"]
    write(batch)
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        batch = response["Items"]
        write(batch)

def discover_schema(dynamodb_client, table_list):
    """
    creates the Configuration file
        1. all fields will be initially strings (DynamoDB has no explicit schema)
        2. you can manually edit the field types
            pick which one you want as number or dates
        3. use this file as input for the sync mode
    """

    schema = {
        "tables": {}
    }

    for table_name in table_list:
        try:
            file = open(logs.DOMAIN + table_name + ".json", "r")
        except FileNotFoundError:
            # Given empty tables are not downloaded
            # Then there is no file
            continue

        primary_keys = []
        table_description = dynamodb_client.describe_table(TableName=table_name)
        for attribute in table_description["Table"]["KeySchema"]:
            primary_keys.append(attribute["AttributeName"])

        schema["tables"][table_name] = {
            "primary-keys": primary_keys,
            "schema": {}
        }

        line = file.readline()
        while line:
            json_obj = json.loads(line)
            for key in json_obj:
                schema["tables"][table_name]["schema"][key] = "string"
            line = file.readline()

    print(json.dumps(schema, indent=4))

def write_schema(table_name, properties):
    """ write the SCHEMA message for a given table to stdout """

    stdout_json_obj = {
        "type": "SCHEMA",
        "stream": table_name,
        "key_properties": properties["primary-keys"],
        "schema": {
            "properties": {}
        }
    }

    for key, kind in properties["schema"].items():
        stdout_json_obj["schema"]["properties"][key] = _TYPE[kind]

    logs.log_json_obj(table_name + ".stdout", stdout_json_obj)
    print(json.dumps(stdout_json_obj))

def write_records(table_name, properties):
    """ write all the RECORD messages for a given table to stdout """
    special_fields = set()

    file = open(logs.DOMAIN + table_name + ".json", "r")
    line = file.readline()
    while line:
        json_obj = json.loads(line)

        stdout_json_obj = {
            "type": "RECORD",
            "stream": table_name,
            "record": {}
        }

        for key, val in json_obj.items():
            try:
                kind = properties["schema"].get(key)
                if kind == "string":
                    stdout_json_obj["record"][key] = str(val)
                elif kind == "number":
                    stdout_json_obj["record"][key] = std_number(val)
                elif kind == "date-time":
                    stdout_json_obj["record"][key] = std_date(val)
                elif kind in ["set", "list", "list<dict>"]:
                    identifier = str(gen_id())
                    stdout_json_obj["record"][key] = identifier
                    new_table_name = f"{table_name}___{key}"
                    nested_obj = {
                        "source_id": identifier,
                        "value": val
                    }
                    logs.log_json_obj(new_table_name, nested_obj)
                    special_fields.add((new_table_name, kind))
            except UnrecognizedNumber:
                logs.log_error("number: [" + val + "]")
            except UnrecognizedDate:
                logs.log_error("date:   [" + val + "]")
            except ValueError:
                logs.log_error("ValueError:  [" + val + "]")

        logs.log_json_obj(table_name + ".stdout", stdout_json_obj)
        print(json.dumps(stdout_json_obj))

        line = file.readline()

    return special_fields

def transform_nested_objects(table_name, kind): # pylint: disable=R0914, R0915
    """
        When this tap finds a nested object instead of a value:

            -------example_table-------
              ColumnA   |   ColumnB
                123     | {6, 2, "ejm"}

        Then it replaces the nested object in ColumnB with an identifier (type string)
        It does so because relational databases like redshift don't support nested objects )

            -------example_table-------
              ColumnA   |   ColumnB
                123     | id:A2BE3F42

        And inserts a new table:

            ----example_table___ColumnB----
               Source_ID    |     Values
              id:A2BE3F42   |       6
              id:A2BE3F42   |       2
              id:A2BE3F42   |     "ejm"

        You can later do look ups by JOIN on Source_ID
    """
    def type_str(obj):
        """ returns a string with the python type of an object """
        if isinstance(obj, str) and is_date(obj):
            return "datetime"
        return type(obj).__name__
    def is_date(date):
        """ detects if a string can be converted to an RFC3339 date """
        try:
            std_date(date)
            return True
        except UnrecognizedDate:
            pass
        return False
    def map_types(type_str):
        map_types = {
            "str": {"type": "string"},
            "int": {"type": "number"},
            "bool": {"type": "boolean"},
            "float": {"type": "number"},
            "datetime": {"type": "string", "format": "date-time"},
        }
        return map_types[type_str]
    def load_records():
        """ load records from file into memory """

        records = []

        # every line contains
        #   { "source_id": identifier, "value": nested_obj }
        #   where nested_obj is a string representing the object to denest

        with open(f"{logs.DOMAIN}{table_name}.json", "r") as file:
            line = file.readline()
            while line:
                json_obj = json.loads(line)
                source_id = json_obj["source_id"]
                nested_str = json_obj["value"]
                nested_str = re.sub(r"(Decimal\()(.{0,10})(\))", r"\g<2>", nested_str)
                nested_obj = ast.literal_eval(nested_str)
                records.append((source_id, nested_obj))
                line = file.readline()
        return records
    def base_singer_record():
        """ returns a base singer record """
        singer_record = {
            "type": "RECORD",
            "stream": table_name,
            "record": {
                "__source_id": source_id
            }
        }
        return singer_record
    def denest_list_schema(nested_obj):
        """ linearizes a set or list given its elements are any primitive types """
        properties = set()
        for elem in nested_obj:
            elem_type = type_str(elem)
            field_name = f"{table_name}__{elem_type}"
            properties.add((field_name, elem_type))
        return {f: map_types(t) for f, t in properties}
    def denest_list_record(elem):
        """ linearizes a set or list given its elements are any primitive types """
        singer_record = base_singer_record()
        field_name = f"{table_name}__{type_str(elem)}"
        singer_record["record"][field_name] = elem
        return singer_record
    def denest_list_dict_schema(nested_obj):
        """ linearizes a list<dict> given its elements are any primitive types """
        properties = set()
        for elem in nested_obj:
            for key, val in elem.items():
                val_type = type_str(val)
                field_name = f"{key}__{val_type}"
                properties.add((field_name, val_type))
        return {f: map_types(t) for f, t in properties}
    def denest_list_dict_record(elem):
        """ linearizes a list<dict> given its elements are any primitive types """
        singer_record = base_singer_record()
        for key, val in elem.items():
            val_type = type_str(val)
            field_name = f"{key}__{type_str(val)}"
            if val_type == "datetime":
                try:
                    singer_record["record"][field_name] = std_date(val)
                except UnrecognizedDate:
                    pass
            else:
                singer_record["record"][field_name] = val
        return singer_record

    # variables
    records = load_records()

    # schema
    singer_schema = {
        "type": "SCHEMA",
        "stream": table_name,
        "key_properties": [],
        "schema": {
            "properties": {}
        }
    }
    for source_id, nested_obj in records:
        if kind in ["set", "list"]:
            singer_schema["schema"]["properties"] = denest_list_schema(nested_obj)
        if kind in ["list<dict>"]:
            singer_schema["schema"]["properties"] = denest_list_dict_schema(nested_obj)

    singer_schema["schema"]["properties"]["__source_id"] = map_types("str")
    print(json.dumps(singer_schema))

    # records
    for source_id, nested_obj  in records:
        for elem in nested_obj:
            if kind in ["set", "list"]:
                singer_record = denest_list_record(elem)
            elif kind in ["list<dict>"]:
                singer_record = denest_list_dict_record(elem)
            print(json.dumps(singer_record))

def std_structure(obj):
    """
    turns a graph to a plain text representation
        nodes may be (list, dict, set, or str)
    """

    logs.log_conversions("special [" + str(obj) + "]")

    def simplify(obj):
        """ aux function to do the heavy lifting """
        structure = ""
        if isinstance(obj, (list, set)):
            for elem in obj:
                structure += simplify(elem) + ","
            structure = structure[:-1]
        elif isinstance(obj, dict):
            for key, val in obj.items():
                structure += key + ":" + simplify(val) + "-"
            structure = structure[:-1]
        else:
            obj_str = re.sub(r"(,|-|:)", r"", str(obj))
            structure = obj_str
        return structure

    new_structure = simplify(obj)

    logs.log_conversions("        [" + new_structure + "]")

    return new_structure

def std_date(date):
    """
    returns a json schema compliant date (RFC 3339)

    standard: https://tools.ietf.org/html/rfc3339#section-5.6
    """

    def month_to_number(month):
        """ returns the month number for a given month name """
        correlation = {"jan": "01",
                       "feb": "02",
                       "mar": "03",
                       "apr": "04",
                       "may": "05",
                       "jun": "06",
                       "jul": "07",
                       "aug": "08",
                       "sep": "09",
                       "oct": "10",
                       "nov": "11",
                       "dec": "12"}
        for month_name, month_number in correlation.items():
            if month_name in month.lower():
                return month_number
        return "err"

    # log it
    logs.log_conversions("date [" + date + "]")

    new_date = ""
    # Dec 31, 2018
    if re.match("([a-zA-Z]{3} [0-9]{2}, [0-9]{4})", date):
        new_date = date[8:12] + "-"
        new_date += month_to_number(date[0:3]) + "-"
        new_date += date[4:6] + "T00:00:00Z"
    # 2018 12 31 or 2018/12/31 or 2018-12-31
    elif re.match("([0-9]{4}( |/|-)[0-9]{2}( |/|-)[0-9]{2})", date):
        new_date = date[0:10] + "T00:00:00Z"
    # 12 31 2018 or 12/31/2018 or 12-31-2018
    elif re.match("([0-9]{2}( |/|-)[0-9]{2}( |/|-)[0-9]{4})", date):
        new_date = date[6:10] + "-" + date[3:5] + "-" + date[0:2] + "T00:00:00Z"
    # Nov 2024
    elif re.match("([a-zA-Z]{3} [0-9]{4})", date):
        new_date = date[4:8] + "-"
        new_date += month_to_number(date[0:3]) + "-"
        new_date += "01T00:00:00Z"
    # 19:27 represents an hour
    elif re.match("([0-9]{2}:[0-9]{2})", date):
        new_date = "1900-01-01T" + date[0:5] + ":00Z"
    # User didn't fill the field
    elif not date:
        new_date = "1900-01-01T00:00:00Z"
    # Not found
    else:
        raise UnrecognizedDate

    # log it
    logs.log_conversions("     [" + new_date + "]")

    return new_date

def std_number(number):
    """ returns a json schema compliant number """
    # log it
    logs.log_conversions("number [" + str(number) + "]")

    # type null instead of str
    if not isinstance(number, str):
        return 0.0

    # point is the decimal separator
    number = number.replace(",", ".")

    # clean typos
    new_number = ""
    for char in number:
        if char in "+-01234567890.":
            new_number += char
    number = new_number

    # no numeric chars after cleaning
    if not number:
        raise UnrecognizedNumber

    # seems ok, lets try
    try:
        number = float(number)
    except:
        raise UnrecognizedNumber

    # log it
    logs.log_conversions("       [" + str(number) + "]")

    return number

class UnrecognizedNumber(Exception):
    """ Raised when tap didn't find a conversion """

class UnrecognizedDate(Exception):
    """ Raised when tap didn't find a conversion """

def arguments_error(parser):
    """ Print help and exit """
    parser.print_help()
    exit(1)

def main():
    """ usual entry point """

    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-auth',
        help='JSON authentication file',
        type=argparse.FileType('r'))
    parser.add_argument(
        '-conf',
        help='JSON config file',
        type=argparse.FileType('r'))
    parser.add_argument(
        '-disc',
        help='Runs the script in discovery mode (generates a customizable CONF file)',
        dest='discovery_mode',
        action='store_true')
    args = parser.parse_args()

    if not args.auth:
        arguments_error(parser)

    auth_keys = json.load(args.auth)

    if args.conf:
        conf_sett = json.load(args.conf)
    else:
        arguments_error(parser)

    # ==== AWS DynamoDB  =======================================================
    # write_schema and write_records don't consume quota
    # table_list and discover_schema consumes negligible quota
    # write_queries consumes quota proportional to the table size
    (dynamodb_client, dynamodb_resource) = create_access_point(auth_keys)

    if args.discovery_mode:
        table_list = get_all_tables(dynamodb_client)

        for table_name, properties in conf_sett["tables"].items():
            write_queries(dynamodb_resource, table_name)

        discover_schema(dynamodb_client, table_list)
    else:
        for table_name, properties in conf_sett["tables"].items():
            write_queries(dynamodb_resource, table_name)
            try:
                write_schema(table_name, properties)
                special_fields = write_records(table_name, properties)
                for new_table_name, kind in special_fields:
                    transform_nested_objects(new_table_name, kind)
            # empty tables are not downloaded
            except FileNotFoundError:
                pass

if __name__ == "__main__":
    main()
