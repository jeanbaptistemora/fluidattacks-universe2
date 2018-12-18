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

import boto3 as AWS_SDK

from . import logs

_TYPE = {
    "string": {"type": "string"},
    "special": {"type": "string"},
    "number": {"type": "number"},
    "date-time": {"type": "string", "format": "date-time"},
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
            for key in json_obj.items():
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
                elif kind == "special":
                    # replaces Decimal('***') by '***' which can be structured by literal_eval
                    new_val = re.sub(r"(Decimal\()(.{0,10})(\))", r"\g<2>", val)
                    val_obj = ast.literal_eval(new_val)
                    stdout_json_obj["record"][key] = std_structure(val_obj)
            except UnrecognizedNumber:
                logs.log_error("number: [" + val + "]")
            except UnrecognizedDate:
                logs.log_error("date:   [" + val + "]")
            except ValueError:
                logs.log_error("ValueError:  [" + val + "]")

        logs.log_json_obj(table_name + ".stdout", stdout_json_obj)
        print(json.dumps(stdout_json_obj))

        line = file.readline()

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

    if not args.discovery_mode:
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
                write_records(table_name, properties)
            # empty tables are not downloaded
            except FileNotFoundError:
                pass

if __name__ == "__main__":
    main()
